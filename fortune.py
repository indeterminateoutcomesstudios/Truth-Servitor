#Truth Servitor "Fortune" version 4.0
#Changes - Refined search functions
#        - Implemented Wolfram|Alpha and Wikipedia search capability.
#        - Implemented OpenWeatherMap Weather search capability
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
import wolframalpha
import wikipedia
import pyowm
# OPTIONAL : If you're going to train Fortune on the basic corpus, uncomment 20.
#from chatterbot.trainers import ChatterBotCorpusTrainer

# external file import
import fortune_io

# general : set bot prefix and retrieve discord token
BOT_PREFIX = ("?")

with open('./token') as tf:
    TOKEN = tf.read().strip()

# retrieve Wolfram|Alpha app ID
with open('./wolfram_app_id') as wai:
    appID = wai.read().strip()

# retrieve OpenWeatherMap API key
with open('./owm_key') as owm:
    wappID = owm.read().strip()

# client/startup
client = Bot(command_prefix=BOT_PREFIX)

# initialize Fortune as ChatterBot client
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

# initialize Fortune as Wolfram|Alpha client
fortuneclient = wolframalpha.Client(appID)

# initialize Fortune as OpenWeatherMap client
fortuneweather = pyowm.OWM(wappID)

# set the trainer
# OPTIONAL : Uncomment 62 and 63 to train Fortune on a basic corpus.
#fortunebot.set_trainer(ChatterBotCorpusTrainer)
#fortunebot.train('chatterbot.corpus.english')

# clientside stuff. tells what the bot's up to behind the scenes.
# This lists Fortune's username, client ID, current time, current servers in terminal
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
    # This line prunes out the mention to the bot
    txt = message.content.replace(message.guild.me.mention,'') if message.guild else message.content
    # This line prevents the bot from replying to itself
    if not message.author.bot and (message.guild == None or client.user in message.mentions):
        # Retrieve the response from the database & send it off
        response=fortunebot.get_response(txt)
        await message.channel.send(response)
    # IMPORTANT : The below line is not a duplicate! This line helps Fortune exit the
    #             on_message function in order to parse commands. If you move it or
    #             delete it, the client commands may not work!
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
        await ctx.send("What are you trying to pull, Xeno? Next you'll be asking me about ~~Squats~~ `REDACTED`...")

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
# MUST HAVE ROLE "BOTMASTER" TO USE
@client.command(aliases=["dev_sd"])
@discord.ext.commands.has_role('Botmaster')
async def shutdown(ctx):
    await ctx.send("Shutting down. Bye!")
    await client.logout()
    await client.close()

# dev tool | command status: set game status of bot
# MUST HAVE ROLE "BOTMASTER" TO USE
@client.command()
@discord.ext.commands.has_role('Botmaster')
async def status(ctx):
    await client.change_presence(activity=discord.Game(name=ctx.message.content[7:]))

# command joke: prints random joke - use at own risk
@client.command()
async def joke(ctx):
    makeJoke = requests.get('http://api.icndb.com/jokes/random?')
    # status code 200 : response sucessful
    if makeJoke.status_code==200:
        makeJoke = makeJoke.json()['value']['joke']
        await ctx.send(makeJoke)
    else:
        # if the status code is anything other than 200 the request failed
        await ctx.send("Sorry, I can't seem to connect right now!")

# command pythonhelp: searches the python docs for help
@client.command(aliases=["pyhelp","ph"])
async def pythonhelp(ctx):
    messagetext = ctx.message.content
    split = messagetext.split(' ')
    if len(split) > 1:
        messagetext = split[1]
        # search the site
        # the python docs site uses some javascript stuff to dynamically load search results
        # as a result BeautifulSoup threw a royal fit and I can't pin down any appropriate tags
        await ctx.send("The top result for that search is: " + 'https://docs.python.org/3/library/' + messagetext + '.html')

# command cpphelp: searches cppreference for help
@client.command(aliases=["cref", "ch"])
async def cpphelp(ctx):
    messagetext = ctx.message.content
    split = messagetext.split(' ')
    if len(split) > 1:
        messagetext = split[1]
        # create the search query
        cpp_search = 'http://en.cppreference.com/mwiki/index.php?title=Special%3ASearch&search=' + messagetext
        # fetch the site
        r = requests.get(cpp_search)
        # parse the site through BeautifulSoup
        soup = BeautifulSoup(r.content, 'html.parser')
        # Narrow down to the div class mw-search-result-heading, grab the first <a href="">
        search_result = soup.find('div', attrs={'class' : 'mw-search-result-heading'}).find('a').get('href')
        # Append the <a href=""> to the appropriate URL
        cpp_result = 'https://en.cppreference.com' + search_result
        # Return the query
        await ctx.send("The top result for that search is: " + cpp_result)

# command stackoverflowhelp: searches stackoverflow for help
# This function is more or less the same as the cppreference one
# see that one's documentation for this one
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

# The Wikipedia and Wolfram|Alpha commands are based off of this:
# https://medium.com/@salisuwy/build-an-ai-assistant-with-wolfram-alpha-and-wikipedia-in-python-d9bc8ac838fe

# command wiki: searches wikipedia
@client.command()
async def wiki(ctx, a):
    # grab the query
    querytext = str(a)
    # run the query
    wiki_search_result = wikipedia.search(querytext)
    # if there is no result:
    if not wiki_search_result:
        await ctx.send("I apologize, but there does not seem to be any information regarding that.")
        return
    # search page try block
    try:
        page = wikipedia.page(wiki_search_result[0])
    except wikipedia.DisambiguationError as err:
        # grab first item on list
        page = wikipedia.page(err.options[0])
    # encode response utf-8
    wikiTitle = str(page.title.encode('utf-8'))
    wikiSummary = str(page.summary.encode('utf-8'))
    # spit the result out prettily
    embed = discord.Embed(title = wikiTitle[1:].strip('\''), color=0x00cc99)
    embed.add_field(name="Summary:", value=wikiSummary[1:]) if len(wikiSummary) < 1020 else embed.add_field(name="Summary:", value=wikiSummary[1:1020] + "...")
    await ctx.send(embed=embed)

# comand wolfram: searches Wolfram|Alpha.
@client.command(aliases=['wolf', 'wa'])
async def wolfram(ctx, a):
    res = fortuneclient.query(a)
    # in the event that Wolfram cannot resolve the question:
    if res['@success'] == 'false':
        await ctx.send("I apologize, but I cannot resolve this query.")
    # otherwise, Wolfram was able to figure it out.
    else:
        result = ''
        # pod[0] is the question
        pod0 = res['pod'][0]
        # pod[1] is the answer with highest confidence
        pod1 = res['pod'][1]
        # check if pod1 has primary=true or title=result|definition
        if(('definition' in pod1['@title'].lower()) or ('result' in pod1['@title'].lower()) or (pod1.get('@primary','false') == 'true')):
            # grab result
            result = resolveListOrDict(pod1['subpod'])
            # spit the result out prettily
            embed = discord.Embed(title = resolveListOrDict(pod0['subpod']), color=0x00cc99)
            embed.add_field(name="Wolfram Says: ", value=result)
            await ctx.send(embed=embed)
        # otherwise we extract Wolfram's question interpretation and throw it to wikipedia
        else:
            question = resolveListOrDict(pod0['subpod'])
            question = removeBrackets(question)
            # in order to call a command function, you have to await/invoke it
            await ctx.invoke(wiki, question)

# supplementary functions to above
def removeBrackets(variable):
    return variable.split('(')[0]
def resolveListOrDict(variable):
    if isinstance(variable, list):
        return variable[0]['plaintext']
    else:
        return variable['plaintext']


# command coinflip: tosses a coin
@client.command()
async def coinflip(ctx):
    flip = random.randint(0,1)
    if(flip == 0):
        await ctx.send("Heads!")
    else:
        await ctx.send("Tails!")

# command time: get the time
# This returns the host's server time.
@client.command(aliases=["gtime"])
async def gt(ctx):
    t = dt.datetime.now().time()
    t = t.strftime('%H:%M:%S')
    await ctx.send("It is currently " + t + ", {}".format(ctx.author.mention))

# command heresy: declare a member a heretic
@client.command(aliases=["heresy"])
async def declareHeresy(ctx, a: discord.Member):
    member_name_string = str(a)
    if(re.match("Fortune", member_name_string)):
        await ctx.send("I am not a heretic, {}".format(ctx.author.mention))
    else:
        await ctx.send("<:heresy:313850309489459200> " + a.mention + " is a heretic. <:heresy:313850309489459200>")

#command weather: gives the weather for a given location
@client.command()
async def weather(ctx, a):
    # get the overall object from pyowm
    observation = fortuneweather.weather_at_place(a)
    w = observation.get_weather()
    # detailed status
    w_status = w.get_detailed_status()
    # reference time
    reftime = w.get_reference_time(timeformat='iso')
    # wind speed & direction
    wind = w.get_wind()
    windspeed = wind.get('speed')
    winddeg = wind.get('deg')
    # humidity
    humidity = w.get_humidity()
    # temperature in celsius - get_temperature returns a dict() object
    ctemperature = w.get_temperature('celsius')
    ctemp = ctemperature.get('temp')
    ctemp_max = ctemperature.get('temp_max')
    ctemp_min = ctemperature.get('temp_min')
    # temperature in fahrenheit
    ftemperature = w.get_temperature('fahrenheit')
    ftemp = ftemperature.get('temp')
    ftemp_max = ftemperature.get('temp_max')
    ftemp_min = ftemperature.get('temp_min')
    # sunrise and sunset times
    sunrise = w.get_sunrise_time(timeformat='iso')
    sunset = w.get_sunset_time(timeformat='iso')
    # output it all pretty-like
    embed = discord.Embed(title = "Weather for " + a, color=0x00cc99)
    embed.add_field(name="Current: ", value=w_status, inline=False)
    embed.add_field(name="Reference Time: ", value=reftime)
    embed.add_field(name="Wind Speed: ", value=windspeed)
    embed.add_field(name="Wind Direction (degrees): " , value=winddeg)
    embed.add_field(name="Humidity (%): ", value=humidity)
    embed.add_field(name="Temperature (C): ", value=ctemp)
    embed.add_field(name="Low (C): ", value=ctemp_min)
    embed.add_field(name="High (C): ", value=ctemp_max)
    embed.add_field(name="Temperature (F): ", value=ftemp, inline=False)
    embed.add_field(name="Low (F): ", value=ftemp_min)
    embed.add_field(name="High (F):", value=ftemp_max)
    embed.add_field(name="Sunrise Time: ", value=sunrise)
    embed.add_field(name="Sunset Time: ", value=sunset)
    await ctx.send(embed=embed)

# command info: tells you about this bot
@client.command()
async def info(ctx):
    embed = discord.Embed(title="Truth Servitor \"Fortune\"", description="Speaks only the truth.", color=0x00cc99)
    embed.add_field(name="Version", value="4.0")
    embed.add_field(name="Author", value="Esherymack | Madison Tibbett")
    embed.add_field(name="Server count", value=f"{len(client.guilds)}")
    embed.add_field(name="Github", value="https://github.com/Esherymack/Truth-Servitor")
    embed.add_field(name="Changes", value="-Wikipedia, Wolfram|Alpha, and OpenWeather implemented.", inline=False)
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
    embed.add_field(name="?shutdown", value="Shuts the bot down. Must have requisite role \"Botmaster.\"", inline=False)
    embed.add_field(name="?status", value="Sets the in-game status of the bot. Must have requisite role \"Botmaster.\"", inline=False)
    embed.add_field(name="?joke", value="Tells a joke. Use at own risk. They are awful.", inline=False)
    embed.add_field(name="?pythonhelp | pyhelp | ph", value="Search the Python Documentation for a string.", inline=False)
    embed.add_field(name="?cpphelp | cref | ch", value="Search cppreference for a string.", inline=False)
    embed.add_field(name="?stackoverflowhelp | stackh | sh", value="Search Stack Overflow for a string.", inline=False)
    embed.add_field(name="?wiki", value="Search Wikipedia", inline=False)
    embed.add_field(name="?wolfram | wolf | wa", value="Query Wolfram|Alpha.", inline=False)
    embed.add_field(name="?weather <LOCATION>", value="Query OpenWeatherMap.", inline=False)
    embed.add_field(name="?coinflip", value="Toss a coin.", inline=False)
    embed.add_field(name="?gt | gtime", value="Display the time.", inline=False)
    embed.add_field(name="?info", value="Gives info regarding this servitor's development.", inline=False)
    embed.add_field(name="?help", value="Gives this message.", inline=False)
    await ctx.send(embed=embed)

client.loop.create_task(on_ready())

client.run(TOKEN)
