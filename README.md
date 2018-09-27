# Truth Servitor/"Fortune" - memey warhammer discord bot - python 3

Truth-Servitor (properly named "Fortune") is a loosely Warhammer themed Discord bot. He is written in Python 3.

### **Required Libraries:**
* os
* discord ([use Discordpy rewrite](https://github.com/Rapptz/discord.py/tree/rewrite))
* requests
* datetime
* re
* random
* Beautiful Soup 4 ([read all about it here](https://www.crummy.com/software/BeautifulSoup/bs4/doc/))
* wolframalpha (`pip install wolframalpha`)
* wikipedia (`pip install wikipedia`)
* pyowm (`pip install pyowm`)
* selenium (`pip install selenium`)

### **Other Things You Need:**
* A Discord bot token
* A WolframAlpha API token
* An OpenWeatherMap API token
* PhantomJS ([get it here](http://phantomjs.org/download.html))

### Usage

Place your bot token into an external file called "token."
Bot tokens may be acquired from [here](https://discordapp.com/developers/applications/me) after creating a Discord application.

Place your WolframAlpha API token into an external file called "wolfram_app_id."
WolframAlpha API tokens may be acquired from [here](http://developer.wolframalpha.com/portal/myapps/index.html) after creating a WolframAlpha ID and creating a new application.

Place your OpenWeatherMap API token into an external file called "owm_key."
OpenWeatherMap tokens may be aquired from [here](http://openweathermap.org/).

Place the filepath to PhantomJS on line 328. It should read something to the effect:

`driver = webdriver.PhantomJS(executable_path=r'C:\Users\Madison\Downloads\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs.exe')`

Lauch from within directory: `python fortune.py`.

#### Current Functions

* Mentioning Fortune in chat will directly speak to him. This functions through Chatterbot. The bot will not speak when not mentioned, but will pick up and "learn" all conversation around him. **THIS FEATURE HAS BEEN REMOVED. THE ORIGINAL CODE IS STILL PRESENT, BUT COMMENTED OUT. THIS IS ONLY FOR REFERENCE.**
* ?fortune or ?wf FILENAME: Picks a fortune from a given file. Defaults to a Warhammer quote from included 'warhammer' binary. This is very similar to Unix `fortune`
* ?exterminatus or ?exterm or ?ex : Declares exterminatus. Edit this text to fit your server's needs.
* ?heresy NAME : Case-sensitive. Declares a member a heretic for all to see. Must use the user's Discord username, not nickname.
* ?shutdown : Shuts the bot down from within Discord. TO USE THIS COMMAND, YOU MUST HAVE THE ROLE "Botmaster."
* ?status <string> : Set the in-game status of the bot. TO USE THIS COMMAND, YOU MUST HAVE THE ROLE "Botmaster."
* ?joke : Tells a Chuck Norris joke. Use at own risk. They're awful.
* ?coinflip : Tosses a coin.
* ?gt or ?gtime : Gets current time. Based on host's system time.
* ?info : Gives info regarding development.
* ?help : Displays all functions.
* ?pythonhelp or ?pyhelp or ?ph : Search the Python 3 docs for a string.
* ?cpphelp or ?cref or ?ch : Search cppreference for a string and get the top result.
* ?stackoverflowhelp or ?stackh or ?sh : Search Stack Overflow for a string and get the top result.
* ?alerts : Fetches current alerts for the game Warframe.
* ?wiki : Search Wikipedia and get the top result.
* ?wolfram or ?wolf or ?wa : Query WolframAlpha. If query fails, it gets booted to Wikipedia.
* ?weather LOCATION : Query OpenWeatherMap for a given location.

### Features Coming Soon
* Case insensitivity/nicknames for ?heresy command
