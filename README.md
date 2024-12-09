# BraxCord
**Project Requirements & Features**
----------------------
                                            November 3rd, 2023

**Bot Title:** BraxCord

**Mock Community:**
	BraxCord will be an interactive bot intended for friend servers and online meme communities. Our bot's functionality will provide its members with access to fun interactions with friends through text-based games and features while also providing light moderation features to keep servers in check. 

**Capabilities & Features:**

- **Throw tomatoes** (ex: `!throw {@User}` )
    -	*Complexity:* S
    -	*Functionality:* Subtracts a tomato from a user’s tomato stockpile and posts a message @ing the user with of a tomato gif being thrown at the user. Tomato throwing has a 1-minute cooldown period. 
    -	*Impact on Community:* Keeps interactions with other members playful and lighthearted. A benefit of using the Garden and Farmer’s Market.
    -   *Theft*: When throwing tomatoes at another user, users will lose a random amount of money from their wallet 
- **Garden:** 
    - Commands:
        - `!garden` (returns the current status of garden, plant and water options)
    - *Complexity:* L
    - *Functionality:* Allows user to grow tomatoes to add to their inventory after a certain amount of time has elapsed.
	- *Impact on Community:* Provides users with a low stress way to engage with the bot and build up their in-game inventory.
- **Farmers Market**  ( `!market` )
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
***RECENT CHANGES***

-CONVERGENCE - MERGED INTO MAIN 
-All project files/bot functionalities are accessible through main now! We completed the great merge.
------ 
***STARTING BRANCHES***
- Quinn
  - *sql-database-integration*
- Eli
  - *database-creation*
- Peyton
  - *Pre-Market/Buttons-Test*
- Hal
  - *user-interactions*
----------

**CURRENT BUGS/ISSUES:**
----------------


-----------

**FUTURE TASKS**
-------------
**Space for Brax devs to share future features and development ideas**

-E - Debug custom help command further, I want to figure out why the embeds aren't working as intended. For now- the default help command serves our needs. 

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
  - https://www.freecodecamp.org/news/create-a-discord-bot-with-python
