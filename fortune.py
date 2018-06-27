#Truth Servitor "Fortune" version 3.2
#Changes - Added more fortunes
#        - Updated search functions to grab top result, rather than search page
#Created by Madison Tibbett

# library imports
from discord.ext.commands import Bot
import discord
import requests
from bs4 import BeautifulSoup
import datetime as dt
import re
import random
from chatterbot import ChatBot
#from chatterbot.trainers import ChatterBotCorpusTrainer

# external file imports
import token
import fortune_io

# general shit and discord token
BOT_PREFIX = ("?")

with open('./token') as tf:
    TOKEN = tf.read().strip()

# client/startup
client = Bot(command_prefix=BOT_PREFIX)

# initialize Fortune as ChatterBot
fortunebot = ChatBot('Fortune',
                    storage_adapter="chatterbot.storage.SQLStorageAdapter",
                    logic_adapters=[
                        "chatterbot.logic.MathematicalEvaluation",
                        "chatterbot.logic.BestMatch",
                        "chatterbot.logic.LowConfidenceAdapter"
                    ],
                    input_adapter="chatterbot.input.VariableInputTypeAdapter",
                    output_adapter="chatterbot.output.OutputAdapter",
                    )

# set the trainer
#fortunebot.set_trainer(ChatterBotCorpusTrainer)
#fortunebot.train('chatterbot.corpus.english')

# clientside stuff. tells me what the bot's up to behind the scenes.
# like what servers he's in, cos i don't want no strangers using him yet
@client.event
async def on_ready():
    await client.wait_until_ready()
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

## implementation of ChatterBot machine-learning chatbot.
@client.event
async def on_message(message):
    txt = message.content.replace(message.guild.me.mention,'') if message.guild else message.content
    if not message.author.bot and (message.guild == None or client.user in message.mentions):
        response=fortunebot.get_response(txt)
        await message.channel.send(response)
    await client.process_commands(message)

# command fortune: pick a random fortune from the specified file in the fortunes dir, or default to
# warhammer if none specified
@client.command(aliases=["wf"])
async def fortune(ctx):
    messagetext = ctx.message.content
    split = messagetext.split(' ')
    if len(split) > 1:
        messagetext = split[1]
    # default to warhammer fortunes if no file specified
    else:
        messagetext = 'warhammer'

    # pick a random bit of wisdom from the file
    fortune = fortune_io.get_fortune(messagetext)

    # file was valid
    if fortune:
        # spit it out
        await ctx.send(fortune)
    # invalid file
    else:
        await ctx.send("What are you trying to pull, Xeno? Next you'll be asking me about ~~Squats~~ `*REDACTED`*...")



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
        # search the site
        # the python docs site uses some javascript stuff to dynamically load search results
        # as a result BeautifulSoup threw a royal fit
        await ctx.send("The top result for that search is : " + 'https://docs.python.org/3/library/' + messagetext + '.html')

# command cpphelp: searches cppreference for help
@client.command(aliases=["cref", "ch"])
async def cpphelp(ctx):
    messagetext = ctx.message.content
    split = messagetext.split(' ')
    if len(split) > 1:
        messagetext = split[1]
        cpp_search = 'http://en.cppreference.com/mwiki/index.php?title=Special%3ASearch&search=' + messagetext
        r = requests.get(cpp_search)
        soup = BeautifulSoup(r.content, 'html.parser')
        search_result = soup.find('div', attrs={'class' : 'mw-search-result-heading'}).find('a').get('href')
        cpp_result = 'https://en.cppreference.com' + search_result
        await ctx.send("The top result for that search is: " + cpp_result)

# command stackoverflowhelp: searches stackoverflow for help
@client.command(aliases=["stackh", "sh"])
async def stackoverflowhelp(ctx):
    messagetext = ctx.message.content
    split = messagetext.split(' ')
    if len(split) > 1:
        messagetext = split[1]
        so_search = 'https://stackoverflow.com/search?q=' + messagetext
        r = requests.get(so_search)
        soup = BeautifulSoup(r.content, 'html.parser')
        search_result = soup.find('div', attrs={'class' : 'summary'}).find('a', attrs={'class' : 'question-hyperlink'}).get('href')
        so_result = 'https://stackoverflow.com/' + search_result
        await ctx.send("The top result for that search is: " + so_result)

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
    embed = discord.Embed(title="Truth Servitor \"Fortune\"", description="Speaks only the truth.", color=0x00cc99)
    embed.add_field(name="Version", value="3.2")
    embed.add_field(name="Author", value="Esherymack | Madison Tibbett")
    embed.add_field(name="Server count", value=f"{len(client.guilds)}")
    embed.add_field(name="Github", value="https://github.com/Esherymack/Truth-Servitor")
    embed.add_field(name="Changes", value="-Fortune's fortune library can now be expanded and customized.", inline=False)
    await ctx.send(embed=embed)

# overwrite the help command with something pretty
client.remove_command('help')
@client.command()
async def help(ctx):
    embed = discord.Embed(title="Truth Servitor", description = "Speaks only the truth. Accepted intonations are:", color=0x00cc99)
    embed.add_field(name="@Fortune", value="Mention the Truth Servitor directly to talk to him.", inline=False)
    embed.add_field(name="?fortune | wf <FILE>", value="Gives daily wisdom.", inline=False)
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

client.run(TOKEN)
