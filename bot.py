import logging
import threading
import time
import boto3
from random import choice, randrange, random
from twitchio.ext import commands
from twitchio.channel import Channel
import oracle
from env import env
from text import initial_history


logging.basicConfig(filename='log.log', level=logging.INFO, format='%(levelname)-7s:%(asctime)s> %(message)s', datefmt='%b-%d %H:%M:%S')


class Bot(commands.Bot):
    def __init__(self):
        self.v = '0.2.03'
        self.first_message = 'HeyGuys'
        self.active = True
        self.chatters = []
        self.streamer_here = False
        self.chime_rate = 30*60
        self.inactivity_before_shutdown = 20*60
        self.chime_rate_granularity = 2
        self.streamer = 'mangort'
        self.last_here = time.time()

        self.oracle = oracle.Oracle(40)

        self.name = env.bot_nick
        self.history = initial_history(self.name).split('\n')
        
        super().__init__(
            token=env.tmi_token,
            client_secret=env.client_secret,
            nick=self.name,
            prefix='!',
            initial_channels=[env.channel]
        )

    def default_channel(self):
        if not self.connected_channels:
            logging.warn('Asking for connected_channels when there are none')
        elif len(self.connected_channels) < 1:
            logging.warn('Asking for connected_channels when they are empty')
        else:
            return self.connected_channels[0]
        
    def is_mod(self):
        return True  # TODO Get this info from badge or user

    def is_command(self, content):
        # chr(1) is a Start of Header character that shows up invisibly in /me ACTIONs
        return content[0] in '!/' or content.startswith(chr(1)+'ACTION ')

    def is_emote_command(self, content):
        return content.startswith('mangor7Ban')

    def add_history(self, content, author):
        self.history += [f'{author}: {content}']

    def should_free_respond(self, content, author):
        return self.active and (author in self.chatters or self.nick.lower() in content.lower())

    async def event_ready(self):
        'Called once when the bot goes online.'
        print(f"{self.nick} is online!")

        # Need to do this when no context available
        self.try_send(self.first_message, warning = "EVENT_READY: Couldn't send first message")

    async def event_raw_data(self, data):
        logging.info(data)

    async def event_message(self, msg):
        'Runs every time a message is sent in chat.'

        if not msg.author:
            return # No author. Maybe because from first_message?

        channel = msg.channel
        content = msg.content
        author = msg.author.name
        name = author.lower()
        if name == self.nick.lower():
            return

        if name == self.streamer:
            self.streamer_here = True

        if self.is_command(content):
            await self.handle_commands(msg)
            return

        self.add_history(content, author)

        if self.is_emote_command(content):
            await self.handle_emote_command(channel, content, author)
        elif self.should_free_respond(content, author):
            await self.free_reply(channel, author)

    async def free_reply(self, channel, author):
        response = self.oracle.respond(self.history, self.nick)
        if response:
            if author in response.lower() or author in self.chatters:
                msg = response
            else:
                msg = f'{response} @{author}'
            time.sleep(len(response)*0.01)
            await channel.send(msg)
            self.add_history(msg, self.nick)
        else:
            await channel.send(':|')

    async def handle_emote_command(self, channel, content, author):
        words = content.split(' ')
        if (words[0] == 'mangor7Ban'):
            banned = " ".join(words[1:]).strip()
            if len(banned) == 0:
                await channel.send(f'{author} banned themselves LUL')
            else:
                await channel.send(f'/me {banned} has been banned for {self.random_time()}')

    def random_time(self):
        units = ['frame', 'mushroom second', 'second', 'minute', 'hour', 'day', 'stream', 'week', 'fortnight', 'month', 'year', 'decade', 'lifetime', 'eon']
        unit = choice(units)
        num = randrange(100)
        if num == 1:
            return f'{num} {unit}'
        else:
            return f'{num} {unit}s'

    async def event_raw_usernotice(self, channel: Channel, tags: dict):
        id = tags['msg-id']
        if id == 'raid':
            await channel.send(f'!so {tags["display-name"]}')
        elif id in ['sub', 'resub', 'subgift', 'submysterygift']:
            logging.info("SUB:::")
            logging.info(tags)
            pass # Need to collect groups of gifts into a single message if using this
        elif id == 'host':
            logging.info("HOST:::")
            logging.info(tags)
        elif id == 'announcement':
            logging.info("ANNOUNCE:::")
            logging.info(tags)
        else:
            logging.info("RAW USER NOTICE:::")
            logging.info(tags)
        return await super().event_raw_usernotice(channel, tags)

    async def event_join(self, channel, user):
        name = user.name.lower()
        if name == self.streamer:
            self.streamer_here = True
        elif self.is_mod() and name.startswith('manofsteel'):
            logging.info(f"Attempting ban of {name}")
            await channel.ban_user(user.id)
            

    async def event_part(self, user):
        name = user.name.lower()
        if name == self.streamer:
            self.streamer_here = False

    @commands.command()
    async def version(self, ctx):
        await ctx.send(f'v{self.v}')

    @commands.command()
    async def r(self, ctx):
        if not self.active: return
        await self.free_reply(ctx.channel, ctx.author.name)

    @commands.command()
    async def help(self, ctx):
        await ctx.send(f"{self.name} commands: https://github.com/amcknight/gort/blob/main/Commands.md")

    @commands.command()
    async def enter(self, ctx):
        if self.active:
            await ctx.send(f"/me OOOO I'm already here! OOOO")
        else:
            await ctx.send(f"/me I'm back peepoArrive")
            self.active = True

    @commands.command()
    async def leave(self, ctx):
        if not self.active: return
        await ctx.send(f'/me I\'m out. peepoLeave')
        self.chatters = []
        self.active = False

    @commands.command()
    async def chat(self, ctx):
        if not self.active: return
        author = ctx.author.name
        if author in self.chatters:
            await ctx.send(f"You've already approached me, {author}. Back up a bit! LUL")
        else:
            self.chatters.append(author)
            await ctx.send(f"/me and {author} gathered")

    @commands.command()
    async def unchat(self, ctx):
        if not self.active: return
        author = ctx.author.name
        if author in self.chatters:
            self.chatters.remove(author)
            await ctx.send(f"/me and {author} disbanded")
        else:
            await ctx.send(f"You're not even near me, {author}. Don't worry, we're not chatting! LUL")

    @commands.command()
    async def chime(self, ctx, *args):
        if not self.active: return
        if not self.streamer_here: return
        subcommand = ' '.join(ctx.args).strip()
        if subcommand == 'more':
            self.chime_rate = self.chime_rate / self.chime_rate_granularity
        elif subcommand == 'less':
            self.chime_rate = self.chime_rate * self.chime_rate_granularity
        else:
            await ctx.send("Chime subcommands are '!chime less' or '!chime more'")
        await ctx.send(f"Chime rate is ~{round(self.chime_rate)} seconds")

    @commands.command()
    async def asme(self, ctx):
        if not self.active: return
        author = ctx.author.name
        response = self.oracle.respond(self.history, author)
        if response:
            msg = f'{author}: {response}'
            time.sleep(len(response)*0.01)
            await ctx.send(msg)
        else:
            await ctx.send(':|')

    @commands.command()
    async def haiku(self, ctx, *args):
        if not self.active: return
        topic = ' '.join(ctx.args).strip()
        if not topic:
            await ctx.send(f"Give me a topic to work with")
            return

        h = self.oracle.complete_haiku(topic)
        lines = h.split('\n')

        await ctx.send(f"tThink ~ {topic} ~")
        time.sleep(1)
        for line in lines:
            time.sleep(0.5)
            await ctx.send(f"/me {line.strip()}")

    @commands.command()
    async def best(self, ctx, *args):
        if not self.active: return
        topic = ' '.join(ctx.args).strip()
        response = self.oracle.complete_best3(topic)
        lines = response.split('\n')
        if len(lines) < 3:
            await ctx.send(':|')
        else:
            lines[0] = f'1. {lines[0].strip()}'
            time.sleep(0.5)
            await ctx.send(lines[0].strip())
            time.sleep(0.3)
            await ctx.send(lines[1].strip())
            time.sleep(0.3)
            await ctx.send(lines[2].strip())

    @commands.command()
    async def reset(self, ctx):
        if not self.active: return
        await ctx.send('peepoTrip I am reborn!')
        self.history = []

    @commands.command()
    async def chatting(self, ctx):
        if not self.active: return
        if len(self.chatters) < 1:
            await ctx.send(f"/me isn't chatting")
        elif len(self.chatters) == 1:
            await ctx.send(f"/me is chatting with {self.chatters[0]}")
        elif len(self.chatters) == 2:
            await ctx.send(f"/me is chatting with {self.chatters[0]} and {self.chatters[1]}")
        else:
            await ctx.send(f"/me is chatting with {', '.join(self.chatters[:-1])}, and {self.chatters[-1]}")

    async def event_error(self, error):
        self.try_send(f"/me :boom: :bug: {self.streamer}", warning = f"EVENT_ERROR: {error}")

    def try_send(self, msg, warning = None, error = None):
        channel = self.default_channel()
        if channel:
            self.loop.create_task(channel.send(msg))
            return True
        else:
            if warning:
                print(warning)
                logging.warn(warning)
            if error:
                print(error)
                logging.error(error)
            return False

    def get_region(self):
        return 'us-east-2' # Hardcoded for now
    def get_instance_id(self):
        return 'i-093ad12750a672191' # Hardcoded for now

    def stop_server(self):
        self.try_send(":homes:", warning='Secondly: No channel to mention stopping server in')

        ec2_client = boto3.client('ec2', region_name=self.get_region())
        response = ec2_client.stop_instances(InstanceIds=[self.get_instance_id()])
        code = response['ResponseMetadata']['HTTPStatusCode']
        if code == 200:
            msg = f"EC2 instance is being stopped"
            print(msg)
            logging.info(msg)
        else:
            msg = f"Error (code: {code}) stopping EC2 instance: {response}"
            print(msg)
            logging.error(msg)

    def randomly_chime(self):
        response = self.oracle.respond(self.history, self.nick)
        if response:
            sent = self.try_send(response, warning = 'Secondly: No channel to chime in')
            if sent:
                self.add_history(response, self.nick)

    def secondly(self):
        if self.streamer_here:
            self.last_here = time.time()
        else:
            if time.time() - self.last_here > self.inactivity_before_shutdown:
                self.stop_server()

        if self.active and self.streamer_here:
            if random() < 1.0 / self.chime_rate:
                self.randomly_chime()
            
def periodic(b):
    max_error_count = 5
    error_count = 0
    while True:
        try:
            time.sleep(1)
            b.secondly()
        except Exception as e:
            error_count += 1
            msg = f'SECONDLY EXCEPTION: {type(e)} with {e.args}'
            print(msg)
            logging.warn(msg)
            if error_count > max_error_count:
                msg = f'SECONDLY max warnings ({max_error_count}) reached. Stopping periodic.'
                b.try_send(':clock: :boom:', error=msg)
                break


if __name__ == "__main__":
    bot = Bot()
    t = threading.Thread(target=periodic, args=(bot,), daemon=True)
    t.start()
    bot.run()
