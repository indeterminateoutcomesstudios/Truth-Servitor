#Truth Servitor version 2.0
# Changes - Now runs off of AIML for chat instead of Cleverbot.
#Created by Madison Tibbett

import random
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import discord
import requests
import datetime as dt
import re
import json
import os
import pkg_resources
import aiml

# general shit and discord token
BOT_PREFIX = ("?")
TOKEN = "NDU4NzgzNDg5MDIyNDkyNjc0.DgxyYw.xn9q2Krf-gm2jDKWQRkr4OmyEwc"  # Get at discordapp.com/developers/applications/me

# client/startup
client = Bot(command_prefix=BOT_PREFIX)
user = 'g2qTdVXk3IAW4JOu'
key = 'y3lisSaFLdnevGuUtvlX05TlDUKXRf5u'
k = aiml.Kernel()

# self.client=Bot(command_prefix=BOT_PREFIX)

# clientside stuff. tells me what the bot's up to behind the scenes.
# like what servers he's in, cos i don't want no strangers using him yet
@client.event
async def on_ready():
    await client.wait_until_ready()
    # load AIML kernel
    if os.path.isfile("bot_brain.brn"):
        k.bootstrap(brainFile = "bot_brain.brn")
    else:
        k.bootstrap(learnFiles = "std-startup.xml", commands = "load aiml b")
        k.saveBrain("bot_brain.brn")
    # k.learn("std-startup.xml")
    # k.respond("load aiml b")
    print("Logging in...")
    print("Username: " + str(client.user.name))
    print("Client ID: " + str(client.user.id))
    print(dt.datetime.now().time())
    print("Current Servers:")
    for server in client.guilds:
        print(server.name)
    print("Starting...")
    print("Bot online!")
    print("----------")

## implementation of A.L.I.C.E AIML bot
@client.event
async def on_message(message):
    if not message.author.bot and (message.guild == None or client.user in message.mentions):
        txt = message.content.replace(message.guild.me.mention,'') if message.guild else message.content
        aiml_response = k.respond(txt)
        await message.channel.send(aiml_response)
    await client.process_commands(message)

# command fortune: pick a random fortune from the 'warhammer' binary
@client.command(aliases=["wf"])
async def fortune(ctx):
    # crack that sucker open and pull out all the good stuff
    lines = open('warhammer', encoding='utf-8').readlines()
    # ...and prune it cos it's ugly...
    fortunes = list(map(lambda t: t.strip(''), lines))
    # pick a random bit of wisdom from the file
    wf2 = random.choice(fortunes)
    # spit it out
    await ctx.send(wf2)

# command exterminatus: conduct exterminatus
@client.command(aliases=["exterm","ex"])
async def exterminatus(ctx):
    exterminatus_msg = '''**I have arrived, and it is now that I perform my charge.
    In fealty to the God-Emperor and by the grace of the Golden Throne,
    I declare Exterminatus upon this server.
    I hereby sign the death warrant of an entire server and consign four souls into oblivion.
    May Imperial Justice account in all balance. The Emperor Protects.**'''
    await ctx.send(exterminatus_msg)

# dev tool | command shutdown: shuts down the bot from server
@client.command(aliases=["dev_sd"])
async def shutdown(ctx):
    await ctx.send("Shutting down. Bye!")
    await client.logout()
    await client.close()

# dev tool | command status: set game status of bot
@client.command()
async def status(ctx):
    await client.change_presence(activity=discord.Game(name=ctx.message.content[7:]))

# command joke: prints random joke - use at own risk
@client.command()
async def joke(ctx):
    makeJoke = requests.get('http://api.icndb.com/jokes/random?')
    if makeJoke.status_code==200:
        makeJoke = makeJoke.json()['value']['joke']
        await ctx.send(makeJoke)

# command pythonhelp: searches the python docs for help
@client.command(aliases=["pyhelp","ph"])
async def pythonhelp(ctx):
    messagetext = ctx.message.content
    split = messagetext.split(' ')
    if len(split) > 1:
        messagetext = split[1]
        await ctx.send('https://docs.python.org/3/search.html?q=' + messagetext)

# command cpphelp: searches cppreference for help
@client.command(aliases=["cref", "ch"])
async def cpphelp(ctx):
    messagetext = ctx.message.content
    split = messagetext.split(' ')
    if len(split) > 1:
        messagetext = split[1]
        await ctx.send('http://en.cppreference.com/mwiki/index.php?title=Special%3ASearch&search=' + messagetext)

# command stackoverflowhelp: searches stackoverflow for help
@client.command(aliases=["stackh", "sh"])
async def stackoverflowhelp(ctx):
    messagetext = ctx.message.content
    split = messagetext.split(' ')
    if len(split) > 1:
        messagetext = split[1]
        await ctx.send('https://stackoverflow.com/search?q=' + messagetext)

# command coinflip: tosses a coin
@client.command()
async def coinflip(ctx):
    flip = random.randint(0,1)
    if(flip == 0):
        await ctx.send("Heads!")
    else:
        await ctx.send("Tails!")

# command time: get the time
@client.command(aliases=["gtime"])
async def gt(ctx):
    t = dt.datetime.now().time()
    t = t.strftime('%H:%M:%S')
    await ctx.send("It is currently " + t + ", {}".format(ctx.author.mention))

# utility | command heresy: declare a member a heretic
@client.command(aliases=["heresy"])
async def declareHeresy(ctx, a: discord.Member):
    member_name_string = str(a)
    if(re.match("Fortune", member_name_string)):
        await ctx.send("I am not a heretic, {}".format(ctx.author.mention))
    else:
        await ctx.send("<:heresy:313850309489459200> " + a.mention + " is a heretic. <:heresy:313850309489459200>")

# command info: tells you about this bot
@client.command()
async def info(ctx):
    embed = discord.Embed(title="Truth Servitor", description="Speaks only the truth.", color=0x00cc99)
    embed.add_field(name="Version", value="1.0")
    embed.add_field(name="Author", value="Esherymack | Madison Tibbett")
    embed.add_field(name="Server count", value=f"{len(client.guilds)}")
    await ctx.send(embed=embed)

# overwrite the help command with something pretty
client.remove_command('help')
@client.command()
async def help(ctx):
    embed = discord.Embed(title="Truth Servitor", description = "Speaks only the truth. Accepted intonations are:", color=0x00cc99)
    embed.add_field(name="@Fortune", value="Mention the Truth Servitor directly to talk to him.", inline=False)
    embed.add_field(name="?fortune | wf", value="Gives daily wisdom.", inline=False)
    embed.add_field(name="?exterminatus | exterm | ex", value="Declares exterminatus.", inline=False)
    embed.add_field(name="?heresy <NAME>", value="Declares a member a heretic.", inline=False)
    embed.add_field(name="?shutdown", value="Shuts the bot down.", inline=False)
    embed.add_field(name="?status", value="Sets the in-game status of the bot.", inline=False)
    embed.add_field(name="?joke", value="Tells a joke. Use at own risk. They are awful.", inline=False)
    embed.add_field(name="?pythonhelp | pyhelp | ph", value="Search the Python Documentation for a string.", inline=False)
    embed.add_field(name="?cpphelp | cref | ch", value="Search cppreference for a string.", inline=False)
    embed.add_field(name="?stackoverflowhelp | stackh | sh", value="Search Stack Overflow for a string.", inline=False)
    embed.add_field(name="?coinflip", value="Toss a coin.", inline=False)
    embed.add_field(name="?gt | gtime", value="Display the time.", inline=False)
    embed.add_field(name="?info", value="Gives info regarding this servitor's development.", inline=False)
    embed.add_field(name="?help", value="Gives this message.", inline=False)
    await ctx.send(embed=embed)

client.loop.create_task(on_ready())

requests.post('https://cleverbot.io/1.0/create', json={'user':user, 'key':key, 'nick':'fortune'})

client.run(TOKEN)
