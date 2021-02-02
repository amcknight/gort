import os
import openai
import time
from twitchio.ext import commands
from oracle import ask, respond

import logging
logging.basicConfig(filename='everything.log', encoding='utf-8', level=logging.DEBUG)

bot = commands.Bot(
    # set up the bot
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']]
)

history = ['mangort: Hi guys, this is {bot.nick}.', '{bot.nick}: Hi everyone, how can I help you?']

active = True

first_message = '/me arrived HeyGuys'

@bot.event
async def event_ready():
    'Called once when the bot goes online.'
    print(f"{bot.nick} is online!")
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(os.environ['CHANNEL'], first_message)

@bot.event
async def event_raw_data(data):
    logging.debug(data)

@bot.event
async def event_message(ctx):
    'Runs every time a message is sent in chat.'
    global history

    content = ctx.content
    author = ctx.author.name
    if content != first_message and content[0] != '!':
        history += [f'{author}: {content}']

    if ctx.author.name.lower() == os.environ['BOT_NICK'].lower():
        return

    if bot.nick.lower() in content.lower():
        response = respond(history[1:], author)
        if author in response.lower():
            msg = response
        else:
            msg = f'{response} @{author}'
        time.sleep(len(response)*0.04)
        await ctx.channel.send(msg)

    await bot.handle_commands(ctx)

# @bot.command()
# async def robogort(ctx):
#     global active
#     if not active:
#         return
#     await ctx.send('HeyGuys I\'m mangort\'s robot and I\'m doing my best. I answer questions but know nothing after Oct 2019 and have no short term memory because mangort hates me and didn\'t build it! :(')

# @bot.command()
# async def leave(ctx):
#     global active
#     if not active:
#         return
#     await ctx.send(f'/me I\'m out. peepoLeave')
#     active = False

# @bot.command()
# async def enter(ctx):
#     global active
#     if active:
#         await ctx.send(f'OOOO {ctx.author.name} OOOO')
#     else:
#         await ctx.send(f"/me I'm back peepoArrive")
#         active = True

@bot.command()
async def talk(ctx):
    global active
    if not active:
        return
    response = respond(history[1:])
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
    print("ERRORRRING")
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

if __name__ == "__main__":
    bot.run()
