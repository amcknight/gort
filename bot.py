import os
import time
import logging
import openai
from random import choice, randrange
from twitchio.ext import commands
from oracle import ask, respond, complete_haiku, complete_best3
from text import initial_history

logging.basicConfig(filename='everything.log', level=logging.INFO)

class Bot(commands.Bot):
    def __init__(self):
        self.first_message = 'HeyGuys'
        self.active = True
        self.chatters = []
        
        name = os.environ['BOT_NICK']
        self.history = initial_history(name).split('\n')
        
        super().__init__(
            token=os.environ['TMI_TOKEN'],
            client_id=os.environ['CLIENT_ID'],
            nick=name,
            prefix=os.environ['BOT_PREFIX'],
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

    async def event_message(self, ctx):
        'Runs every time a message is sent in chat.'

        if not ctx.author:
            return # No author. Maybe because from first_message?
        author = ctx.author.name
        if author.lower() == self.nick.lower():
            return

        content = ctx.content
        if self.is_command(content):
            await self.handle_commands(ctx)
            return

        self.add_history(content, author)

        if self.is_emote_command(content):
            await self.handle_emote_command(ctx)
        elif self.should_free_respond(content, author):
            await self.free_reply(ctx)

    async def free_reply(self, ctx):
        author = ctx.author.name
        response = respond(self.history, self.nick)
        if response:
            if author in response.lower() or author in self.chatters:
                msg = response
            else:
                msg = f'{response} @{author}'
            time.sleep(len(response)*0.01)
            await ctx.channel.send(msg)
            self.add_history(msg, self.nick)
        else:
            await ctx.channel.send(':|')

    async def handle_emote_command(self, ctx):
        words = ctx.content.split(' ')
        if (words[0] == 'mangor7Ban'):
            banned = " ".join(words[1:]).strip()
            if len(banned) == 0:
                pass
            else:
                await ctx.channel.send(f'/me {banned} has been banned for {self.random_time()}')

    def random_time(self):
        units = ['frame', 'mushroom second', 'second', 'minute', 'hour', 'day', 'week', 'month', 'year', 'decade', 'eon']
        unit = choice(units)
        num = randrange(100)
        if num == 1:
            return f'{num} {unit}'
        else:
            return f'{num} {unit}s'

    async def event_join(self, channel, user):
        if channel.name == 'mangort':
            pass # A user joined

    @commands.command()
    async def r(self, ctx):
        if not self.active:
            return
        await self.free_reply(ctx)

    @commands.command()
    async def robogort(self, ctx):
        if not self.active:
            return
        await ctx.send(f"Hi {ctx.author.name}! I'm mangort's robot. I'll respond to you when you use my name or !r. I'm trained on the ENTIRE internet so can get pretty offensive so be warned!. Type !help to see what I can do.")

    @commands.command()
    async def help(self, ctx):
        await ctx.send("Commands: !leave -> I'll leave the room, !enter -> I'll enter the room, !chat -> I'll respond to everything you say without you calling my name, !unchat -> I'll only respond to you when you use my name, !reset I'll wipe my short term memory")

    @commands.command()
    async def enter(self, ctx):
        if self.active:
            await ctx.send(f"/me OOOO I'm already here! OOOO")
        else:
            await ctx.send(f"/me I'm back peepoArrive")
            self.active = True

    @commands.command()
    async def leave(self, ctx):
        if not self.active:
            await ctx.send(f"/me isn't here, {ctx.author.name}")
        else:
            await ctx.send(f'/me I\'m out. peepoLeave')
            self.chatters = []
        self.active = False

    @commands.command()
    async def chat(self, ctx):
        author = ctx.author.name
        if not self.active:
            await ctx.send(f"/me isn't here, {author}")
            return

        if author in self.chatters:
            await ctx.send(f"You've already approached me, {author}. Back up a bit! LUL")
        else:
            self.chatters.append(author)
            await ctx.send(f"/me and {author} gathered")

    @commands.command()
    async def unchat(self, ctx):
        author = ctx.author.name
        if not self.active:
            await ctx.send(f"/me isn't here, {author}")
            return

        if author in self.chatters:
            self.chatters.remove(author)
            await ctx.send(f"/me and {author} disbanded")
        else:
            await ctx.send(f"You're not even near me, {author}. Don't worry, we're not chatting! LUL")

    @commands.command()
    async def asme(self, ctx):
        if not self.active:
            return

        author = ctx.author.name
        response = respond(self.history, author)
        if response:
            msg = f'{author}: {response}'
            time.sleep(len(response)*0.01)
            await ctx.channel.send(msg)
        else:
            await ctx.channel.send(':|')

    @commands.command()
    async def haiku(self, ctx, *args):
        if not self.active:
            return

        topic = ' '.join(ctx.args).strip()

        h = complete_haiku(topic)
        lines = h.split('\n')

        await ctx.send(f"pepegeHmm ~ {topic} ~")
        time.sleep(1)
        for line in lines:
            time.sleep(0.5)
            await ctx.send(f"/me {line.strip()}")

    @commands.command()
    async def best(self, ctx, *args):
        if not self.active:
            return

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
        print("RESET")
        if not self.active:
            return
        await ctx.channel.send('peepoTrip I\'m reborn!')
        self.history = []

    @commands.command()
    async def chatting(self, ctx):
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
