# Truth Servitor/"Fortune" - memey warhammer discord bot - python 3

Truth-Servitor (properly named "Fortune") is a loosely Warhammer themed Discord chatbot.

### **Required Libraries:**
* random
* asyncio
* discord ([use Discordpy rewrite](https://github.com/Rapptz/discord.py/tree/rewrite))
* requests
* datetime
* re
* json
* os
* pkg_resources
* Chatterbot ([get it here](https://github.com/gunthercox/ChatterBot))


### Usage

Replace the `<TOKEN GOES HERE>` on line 20 with your bot token.
Bot tokens may be acquired from [here](discordapp.com/developers/applications/me) after creating a Discord application.

Lauch from within directory: `python fortune.py`.

On first launch, a Sqlite file called `db.sqlite3` will be generated. This is the bot's "brain." It will record any and all conversation held in Discord.

**You can disable Fortune's constant spam of "I'm sorry, I don't understand" while it is learning by commenting out line 66.**

#### Current Functions

* ~~Mentioning Fortune in chat will directly speak to him~~. *Currently will respond to any message sent in Discord to fascilitate learning.* This functions through Chatterbot.
* ?fortune or ?wf : Picks a random Warhammer quote from the included "warhammer" binary file. This is very similar to Unix `fortune`
* ?exterminatus or ?exterm or ?ex : Declares exterminatus. Edit this text to fit your server's needs.
* ?heresy <NAME> : Case-sensitive. Declares a member a heretic for all to see.
* ?shutdown : Shuts the bot down from within Discord.
* ?status <string> : Set the in-game status of the bot. 
* ?joke : Tells a Chuck Norris joke. Use at own risk. They're awful.
* ?coinflip : Tosses a coin.
* ?gt or ?gtime : Gets current time. Based on host's system time.
* ?info : Gives info regarding development.
* ?help : Displays all functions.

**Currently Under Construction: These functions may change for convenience later on to give the first result of a search, not the search page itself.**
* ?pythonhelp or ?pyhelp or ?ph : Search the Python Documetation for a given string.
* ?cpphelp or ?cref or ?ch : Search CPPReference for a string.
* ?stackoverflowhelp or ?stackh or ?sh : Search Stack Overflow for a string.

### Features Coming Soon
* Wolfram Alpha search 
* More fortunes

