import os
import time
import logging
import openai
from random import choice, randrange
from twitchio.ext import commands
from twitchio.channel import Channel
from oracle import ask, respond, complete_haiku, complete_best3
from text import initial_history

logging.basicConfig(filename='everything.log', level=logging.INFO)

class Bot(commands.Bot):
    def __init__(self):
        self.v = '0.1.06'
        self.first_message = 'HeyGuys'
        self.active = True
        self.chatters = []
        
        name = os.environ['BOT_NICK']
        self.history = initial_history(name).split('\n')
        
        super().__init__(
            token=os.environ['TMI_TOKEN'],
            client_id=os.environ['CLIENT_ID'],
            nick=name,
            prefix='!',
            initial_channels=[os.environ['CHANNEL']]
        )

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
        await self.connected_channels[0].send(self.first_message) # Need to do this when no context available

    async def event_raw_data(self, data):
        logging.info(data)

    async def event_message(self, msg):
        'Runs every time a message is sent in chat.'

        if not msg.author:
            return # No author. Maybe because from first_message?

        channel = msg.channel
        content = msg.content
        author = msg.author.name
        if author.lower() == self.nick.lower():
            return

        if self.is_command(content):
            await self.handle_commands(msg)
            return

        self.add_history(content, author)

        if self.is_emote_command(content):
            await self.handle_emote_command(channel, content, author)
        elif self.should_free_respond(content, author):
            await self.free_reply(channel, author)

    async def free_reply(self, channel, author):
        response = respond(self.history, self.nick)
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
                await channel.send(f'/me {author} banned themselves LUL')
            else:
                await channel.send(f'/me {banned} has been banned for {self.random_time()}')

    def random_time(self):
        units = ['frame', 'mushroom second', 'second', 'minute', 'hour', 'day', 'week', 'month', 'year', 'decade', 'eon']
        unit = choice(units)
        num = randrange(100)
        if num == 1:
            return f'{num} {unit}'
        else:
            return f'{num} {unit}s'

    async def event_raw_usernotice(self, channel: Channel, tags: dict):
        if tags['msg-id'] == 'raid':
            await channel.send(f'!so {tags["display-name"]}')
        elif tags['msg-id'] in ['sub', 'resub', 'subgift', 'submysterygift']:
            logging.info("SUB:::")
            logging.info(tags)
            pass # Need to collect groups of gifts into a single message if using this
        elif tags['msg-id'] == 'host':
            logging.info("HOST:::")
            logging.info(tags)
        elif tags['nsg-id'] == 'announcement':
            logging.info("ANNOUNCE:::")
            logging.info(tags)
        else:
            logging.info("RAW USER NOTICE:::")
            logging.info(tags)
        return await super().event_raw_usernotice(channel, tags)

    @commands.command()
    async def version(self, ctx):
        await ctx.send(f'peepoHmm v{self.v}')

    @commands.command()
    async def r(self, ctx):
        if not self.active: return
        await self.free_reply(ctx.channel, ctx.author.name)

    @commands.command()
    async def help(self, ctx):
        await ctx.send("Robogort commands: https://github.com/amcknight/gort/blob/main/Commands.md")

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
    async def asme(self, ctx):
        if not self.active: return
        author = ctx.author.name
        response = respond(self.history, author)
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

        h = complete_haiku(topic)
        lines = h.split('\n')

        await ctx.send(f"pepegeHmm ~ {topic} ~")
        time.sleep(1)
        for line in lines:
            time.sleep(0.5)
            await ctx.send(f"/me {line.strip()}")

    @commands.command()
    async def best(self, ctx, *args):
        if not self.active: return
        topic = ' '.join(ctx.args).strip()
        response = complete_best3(topic)
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
        await ctx.send('peepoTrip I\'m reborn!')
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
        print(error)
        logging.error(error)
        await self.connected_channels[0].send("/me :boom: PepeHands there are bugs in my brain, mangort")

if __name__ == "__main__":
    Bot().run()
