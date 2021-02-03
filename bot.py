import os
import openai
import time
from twitchio.ext import commands
from oracle import ask, respond

import logging
logging.basicConfig(filename='everything.log', level=logging.INFO)

bot = commands.Bot(
    # set up the bot
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']]
)

history = [f'mangort: Hi guys, this is {bot.nick}.', f'{bot.nick}: Hi everyone, how can I help you?']

active = True
is_chatting = ['mangort']

first_message = '/me arrived HeyGuys'

def is_command(content):
    # chr(1) is a Start of Header character that shows up invisibly in /me ACTIONs
    return content[0] in '!/' or content.startswith(chr(1)+'ACTION ')

def add_history(content, author):
    global history
    if not is_command(content):
        history += [f'{author}: {content}']

def should_free_respond(content, author):
    return active and author in is_chatting or bot.nick.lower() in content.lower()

@bot.event
async def event_ready():
    'Called once when the bot goes online.'
    print(f"{bot.nick} is online!")
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(os.environ['CHANNEL'], first_message)

@bot.event
async def event_raw_data(data):
    logging.info(data)

@bot.event
async def event_message(ctx):
    'Runs every time a message is sent in chat.'
    global history

    content = ctx.content
    author = ctx.author.name

    add_history(content, author)

    if author.lower() == bot.nick.lower():
        return

    if is_command(content):
        await bot.handle_commands(ctx)
        return

    if should_free_respond(content, author):
        response = respond(history[1:], author)
        if response:
            if author in response.lower():
                msg = response
            else:
                msg = f'{response} @{author}'
            time.sleep(len(response)*0.04)
            await ctx.channel.send(msg)
        else:
            await ctx.channel.send(':|')

@bot.command()
async def robogort(ctx):
    global active
    if not active:
        return
    await ctx.send("Hi @{ctx.author.name}! I'm mangort's robot. I'll respond to you when you use my name. I'm trained on the ENTIRE internet so can get pretty offensive. Mangort is working on fixing that but hasn't yet so be warned!. Type !commands to see what I can do.")


@bot.command()
async def commands(ctx):
    await ctx.send("Commands: !leave -> I'll leave the room, !enter -> I'll enter the room, !hi -> I'll respond to everything you say without you calling my name, !bye -> I'll only respond to you when you use my name, !reset I'll wipe my short term memory")

@bot.command()
async def leave(ctx):
    global active
    if not active:
        await ctx.send(f"/me (I'm not here)")
    else:
        await ctx.send(f'/me I\'m out. peepoLeave')
    active = False

@bot.command()
async def enter(ctx):
    global active
    if active:
        await ctx.send(f"/me OOOO I'm already here! OOOO")
    else:
        await ctx.send(f"/me I'm back peepoArrive")
        active = True

@bot.command()
async def talk(ctx):
    global active
    if not active:
        return
    response = respond(history, ctx.author.name)
    await ctx.channel.send(response)

@bot.command()
async def reset(ctx):
    global history
    global active
    if not active:
        return
    await ctx.channel.send('peepoTrip I\'m reborn!')
    history = []

@bot.event
async def event_error(error, data):
    print("ERRORRRING: Need to learn from this event and act on it")
    print(error)

if __name__ == "__main__":
    bot.run()
