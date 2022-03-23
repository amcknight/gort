import os
import openai
import time
from twitchio.ext import commands
from oracle import ask, respond

import logging
logging.basicConfig(filename='everything.log', level=logging.INFO)

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=os.environ['TMI_TOKEN'],
            client_id=os.environ['CLIENT_ID'],
            nick=os.environ['BOT_NICK'],
            prefix=os.environ['BOT_PREFIX'],
            initial_channels=[os.environ['CHANNEL']]
        )
        self.history = [f'mangort: Hi guys, this is {self.nick}.', f'{self.nick}: Hi everyone, how can I help you?']
        self.first_message = 'HeyGuys'
        self.active = True
        self.chatters = []

    def is_command(self, content):
        # chr(1) is a Start of Header character that shows up invisibly in /me ACTIONs
        return content[0] in '!/' or content.startswith(chr(1)+'ACTION ')

    def add_history(self, content, author):
        if not self.is_command(content):
            self.history += [f'{author}: {content}']

    def should_free_respond(self, content, author):
        return self.active and author in self.chatters or self.nick.lower() in content.lower()

    async def event_ready(self):
        'Called once when the bot goes online.'
        print(f"{self.nick} is online!")
        await self.connected_channels[0].send(self.first_message) # Need to do this when no context available

    async def event_raw_data(self, data):
        logging.info(data)

    async def event_message(self, ctx):
        'Runs every time a message is sent in chat.'

        content = ctx.content
        author = ctx.author.name
    
        self.add_history(content, author)

        if author.lower() == self.nick.lower():
            return

        if self.is_command(content):
            await self.handle_commands(ctx)
            return

        if self.should_free_respond(content, author):
            response = respond(self.history[1:], author)
            if response:
                if author in response.lower():
                    msg = response
                else:
                    msg = f'{response} @{author}'
                time.sleep(len(response)*0.04)
                await ctx.channel.send(msg)
            else:
                await ctx.channel.send(':|')

    @commands.command()
    async def robogort(self, ctx):
        if not self.active:
            return
        await ctx.send("Hi @{ctx.author.name}! I'm mangort's robot. I'll respond to you when you use my name. I'm trained on the ENTIRE internet so can get pretty offensive. Mangort is working on fixing that but hasn't yet so be warned!. Type !help to see what I can do.")

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
            await ctx.send(f"/me isn't here, @{ctx.author.name}")
        else:
            await ctx.send(f'/me I\'m out. peepoLeave')
            self.chatters = []
        self.active = False

    @commands.command()
    async def chat(self, ctx):
        author = ctx.author.name
        if not self.active:
            await ctx.send(f"/me isn't here, @{author}")
            return

        if author in self.chatters:
            await ctx.send(f"You've already approached me, @{author}. Back up a bit! LUL")
        else:
            self.chatters.append(author)
            await ctx.send(f"/me and {author} gathered")

    @commands.command()
    async def unchat(self, ctx):
        author = ctx.author.name
        if not self.active:
            await ctx.send(f"/me isn't here, @{author}")
            return

        if author in self.chatters:
            self.chatters.remove(author)
            await ctx.send(f"/me and {author} disbanded")
        else:
            await ctx.send(f"You've already approached me, @{author}. Back up a bit! LUL")

    async def chatting(self, ctx):
        if len(self.chatters) < 1:
            await ctx.send(f"/me isn't chatting")
        elif len(self.chatters) == 1:
            await ctx.send(f"/me is chatting with {self.chatters[0]}")
        else:
            await ctx.send(f"/me is chatting with {', '.join(self.chatters[:-1])}, and {self.chatters[-1]}")

    @commands.command()
    async def reset(self, ctx):
        print("RESET")
        if not self.active:
            return
        await ctx.channel.send('peepoTrip I\'m reborn!')
        self.history = []

    async def event_error(self, error, data):
        print("ERRORRRING: Need to learn from this event and act on it")
        print(error)

if __name__ == "__main__":
    Bot().run()
