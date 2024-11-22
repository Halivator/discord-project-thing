# discord-project-thing

ideas so far:

    - Conomy
    - tomatoTomatoTomato
    - cyber bullying children
    - banning 



Buh.


Discord Bot must:

    • Be connected to a database
        ◦ Can be pregenerated, or not.
        ◦ It’s required
    • Be connected to an API
    • Explain what it does, and why:
        ◦ 
------




**Project 2 Phase 1 Report**
----------------------
                                            November 3rd, 2024


**Bot Title:** BraxCord

**Mock Community:**
	BraxCord will be an interactive bot intended for friend servers and online meme communities. Our bot's functionality will provide its members with access to fun interactions with friends through text-based games and features while also providing light moderation features to keep servers in check. 

**Capabilities & Features:**

- **Theft** (ex: `!steal {@User} {optional:amountToSteal}` )
    -	*Complexity:* S
    -	*Functionality:* Implements the ability to steal from another user’s wallet or inventory. Theft has a cooldown period of one hour (one steal per hour).
    -	**Impact on Community:** Provides users with an interactive way to pull pranks on their friends/other community members. Allows users to take in-game currency and items from other members with a limit to prevent spamming.
- **Throw tomatoes** (ex: `!tomato {@User}` )
    -	*Complexity:* S
    -	*Functionality:* Subtracts a tomato from a user’s tomato stockpile and posts a message @ing the user with of a tomato gif being thrown at the user. Tomato throwing has a 1-minute cooldown period. 
    -	*Impact on Community:* Keeps interactions with other members playful and lighthearted. A benefit of using the Garden and Farmer’s Market.
- **Garden:**
    - Commands:
        - `!garden` (returns the current status of garden, plants, as well as seeds in inventory)
        - `!plant` (to plant 1 tomato plant per use, but they must have a seed!)
    	- `!water` (waters the plant, could potentially spoil plants if watered over 3 times in an hour, or will speed up growth slightly if used less than 3 times.)
    - *Complexity:* L
    - *Functionality:* Allows user to grow tomatoes to add to their inventory after a certain amount of time has elapsed.
	- *Impact on Community:* Provides users with a low stress way to engage with the bot and build up their in-game inventory.
- **Farmers Market**  ( `!buy {amount}` , `!sell {amount}` )
    - *Complexity:* M
	- *Functionality:* To sell tomatoes for in-game currency and to buy seeds
	- *Impact on Community:* Provides users with a fun way to interact with in-game currency/items and continue making a profit.
- **React to User Messages** *(contains a default list, can be customized by server administrators)*
	- *Complexity:* L
	- *Functionality:* If a user says a specific word provided by moderators OR keywords chosen by developers, the bot replies to them with the message contents in some form of media (text, images, video, gifs, etc.). 
	- *Impact on Community:* Provides users access to a partial moderation feature, which can be used alongside administrator-chosen banned words to lightly implement server rules. Otherwise, this acts as a means for playful bot-to-user interactions.
- **Wallet** (ex: `!wallet` )
    - *Complexity:* M
    - *Functionality:* Provides users with access to their total in-game currency and inventory; can be accessed at any time.
    - *Impact on Community:* Provides users with a way to interact with the rest of the game and see the reward of their time using the bot.



------


***BRANCHES***
- Quinn
  - *sql-database-integration*







----------

**CURRENT BUGS/ISSUES:**
----------------
- Q- commands / command prefix does not work. on_message(message) logger shows that messages are being read, but they do not get seen as commands
- Q- app_commands work. However, upon trying to access a local file (see: eightball commands), Discord error: "The application did not respond" occurs.
  - Q- How do we get console output for when these errors occur?
- Q- How does the default help command work? Can we set a custom help command if command prefixes aren't recognized?


-----------

**CURRENT TASKS**
-------------
- Troubleshooting command prefixes (Q) (P)
- Creating Database models and tables for Users, Guilds, UserGuilds via sqlalchemy (E)



---------------

**To-Do**
---------------
- Database
  - tables:
    - Users
    - Guilds
    - UserGuild
    - wallets
  - sqlalchemy, sqlite
- Debugging commands and command prefix





------------------

*Reference Material*
--------------------

- Discord.py documentation
  - More about client.Events
    - https://discordpy.readthedocs.io/en/latest/api.html#discord.Client.event
  - (skip to: app_commands.CommandTree)
    - https://discordpy.readthedocs.io/en/stable/interactions/api.html?highlight=get#discord.app_commands.CommandTree.get_commands
  - More about discord.ext commands
    - https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html#ext-commands-commands
    
- Discord.py examples repo on github
  - see basic example of how app_commands work
  - https://github.com/Rapptz/discord.py/blob/master/examples/app_commands/basic.py
- Github custom Help command using Cogs
  - https://gist.github.com/nonchris/1c7060a14a9d94e7929aa2ef14c41bc2#file-discord-custom-help-command-py-L13
- Paradoxial Youtube Tutorials
  - NOTE: may be outdated due to being 2 years old
  - Part 3: Activity Status
    - https://www.youtube.com/watch?v=Erir7v7YXR8
- Initial code tutorial
  - https://www.freecodecamp.org/news/create-a-discord-bot-with-python/