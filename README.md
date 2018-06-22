# Truth Servitor/"Fortune" - memey warhammer discord bot - python 3 & aiml 

Truth-Servitor (properly named "Fortune") is a loosely Warhammer themed Discord chatbot.

References:

[Dev Dungeon's *Chatty Cathy* Bot](https://github.com/DevDungeon/ChattyCathy)

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
* aiml (use `pip install python-aiml` for python 3, not just `pip install aiml` (that's for python 2))

### Usage

Keep the bot (fortune.py) in the "aiml" directory. Replace the `<TOKEN GOES HERE>` on line 20 with your bot token.
Bot tokens may be acquired from [here](discordapp.com/developers/applications/me) after creating a bot account.

Lauch from within directory: `python fortune.py`.
First launch will generate a `.brn` file from the included AIML modules. This file is the "brain" and helps load the bot faster later.

If custom AIML files are added, keep them in the Custom directory. When new AIML files are added, or when current AIML files are edited, the `.brn` file must be deleted and re-generated. This may be fixed later to do it with a command.

#### Current Functions

* Mentioning Fortune in chat will directly speak to him. This functions on AIML.
* ?fortune or ?wf : Picks a random Warhammer quote from the included "warhammer" binary file. This is very similar to Unix `fortune`
* ?exterminatus or ?exterm or ?ex : Declares exterminatus. Edit this text to fit your server's needs.
* ?heresy <NAME> : Case-sensitive. Declares a member a heretic for all to see.
* ?shutdown : Shuts the bot down from within Discord.
* ?status <string> : Set the in-game status of the bot. 
* ?joke : Tells a Chuck Norris joke. Use at own risk. They're awful.
* ?coinflip : Tosses a coin.
* ?gt or ?gtime : Gets current time. Based on host's system time.
* ?info : Gives info regarding development.
* ?help : Displays all functions.lo

**Currently Under Construction: These functions may change for convenience later on to give the first result of a search, not the search page itself.**
* ?pythonhelp or ?pyhelp or ?ph : Search the Python Documetation for a given string.
* ?cpphelp or ?cref or ?ch : Search CPPReference for a string.
* ?stackoverflowhelp or ?stackh or ?sh : Search Stack Overflow for a string.


