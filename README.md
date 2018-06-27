# Truth Servitor/"Fortune" - memey warhammer discord bot - python 3

Truth-Servitor (properly named "Fortune") is a loosely Warhammer themed Discord chatbot.

### **Required Libraries:**
* os
* discord ([use Discordpy rewrite](https://github.com/Rapptz/discord.py/tree/rewrite))
* requests
* datetime
* re
* random
* Chatterbot ([get it here](https://github.com/gunthercox/ChatterBot))
* Beautiful Soup 4 ([read all about it here](https://www.crummy.com/software/BeautifulSoup/bs4/doc/))

### Usage

Place your bot token into an external file called "token."
Bot tokens may be acquired from [here](https://discordapp.com/developers/applications/me) after creating a Discord application.

Lauch from within directory: `python fortune.py`.

On first launch, a Sqlite file called `db.sqlite3` will be generated. This is the bot's "brain." It will record any and all conversation held in Discord.

#### Current Functions

* Mentioning Fortune in chat will directly speak to him. This functions through Chatterbot. The bot will not speak when not mentioned, but will pick up and "learn" all conversation around him.
* ?fortune or ?wf FILENAME: Picks a fortune from a given file. Defaults to a Warhammer quote from included 'warhammer' binary. This is very similar to Unix `fortune`
* ?exterminatus or ?exterm or ?ex : Declares exterminatus. Edit this text to fit your server's needs.
* ?heresy NAME : Case-sensitive. Declares a member a heretic for all to see. Must use the user's Discord username, not nickname.
* ?shutdown : Shuts the bot down from within Discord.
* ?status <string> : Set the in-game status of the bot.
* ?joke : Tells a Chuck Norris joke. Use at own risk. They're awful.
* ?coinflip : Tosses a coin.
* ?gt or ?gtime : Gets current time. Based on host's system time.
* ?info : Gives info regarding development.
* ?help : Displays all functions.
* ?pythonhelp or ?pyhelp or ?ph : Search the Python 3 docs for a string.
* ?cpphelp or ?cref or ?ch : Search cppreference for a string and get the top result.
* ?stackoverflowhelp or ?stackh or ?sh : Search Stack Overflow for a string and get the top result.

### Features Coming Soon
* Wolfram Alpha search
* Case insensitivity/nicknames for ?heresy command
