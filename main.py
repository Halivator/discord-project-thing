### BraxCord Discord Bot
# main.py
# Created: 11/11/24 ~ 5:21pm
# Last Updated: 11/11/24 ~ 5:21pm

#Q# NOTE: 11/11-Q: tutorial followed for initial code setup below:  (planning to remove some of the comment annotations at a later date)
# https://www.freecodecamp.org/news/create-a-discord-bot-with-python/

#############################################################################

from base import *
from modules import Database
from data_models import UserGuild, Responses, Wallet, Base, async_session, initialize_db
from database_operations import add_to_userguild, get_from_userguild, delete_from_userguild, create_user_wallet, get_user_wallet, update_user_wallet, delete_user_wallet

from dotenv import load_dotenv
import discord 
from discord import app_commands
from discord.ext import commands, tasks

from itertools import cycle
import aiofiles, aiofiles.os
import logging
import logging.handlers
import asyncio
from pycolorise.colors import *
#https://matplotlib.org/stable/gallery/color/named_colors.html

#https://ipython.readthedocs.io/en/4.x/api/generated/IPython.utils.PyColorize.html

import os           #Q# os library is only used to get the TOKEN from the .env file


load_dotenv()


logger = logging.getLogger(__name__)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

#--------------------------------------------------------------
class MyClient(commands.Bot):
    """Class object for the bot"""
    def __init__(self, command_prefix, log_handler, log_level, *, intents: discord.Intents):
        super().__init__(command_prefix=command_prefix, log_handler=log_handler, log_level=log_level, intents= intents)
        # vv from modules import Database
        self.db = Database(Auth.FILENAME)
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        #self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        if (Auth.MY_GUILD == ""):
            self.tree.copy_global_to()
            await self.tree.sync()
        else:
            self.tree.copy_global_to(guild=Auth.MY_GUILD)
            await self.tree.sync(guild=Auth.MY_GUILD)
#--------------------------------------------------------------


intents = discord.Intents.default() #all() #.default()
# set particular Intents                        # https://discordpy.readthedocs.io/en/latest/api.html?highlight=client#intents
intents.message_content = True
intents.members = True
intents.presences = True
intents.guilds = True

bot = MyClient(command_prefix=f'{Auth.COMMAND_PREFIX}',log_handler=handler,log_level=logging.DEBUG,intents=intents) #command_prefix=['$!'],      # https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html#ext-commands-commands

#------------------------------------------------------------------------
#Q# video: Making a Discord Bot in Python (Part 3: Activity Status)
#------------------------------------------------------------------------
status_phrases = [
    f"try {Auth.COMMAND_PREFIX}help",
    f"Throwing tomatoes ({Auth.COMMAND_PREFIX}help)",
    f"Shut up, nerd ({Auth.COMMAND_PREFIX}help)",
    f"Cyberbullying Children ({Auth.COMMAND_PREFIX}help)",
    f"there's no /j here! ({Auth.COMMAND_PREFIX}help)",
    ]
"""List of statuses to cycle through"""

if Auth.DEV_NAME is not None: status_phrases.append(f"developer online: {Auth.DEV_NAME} ({Auth.COMMAND_PREFIX}help)")

bot_status = cycle(status_phrases)

@tasks.loop(seconds = Util.timetick)
async def change_status():
    #print('{bot_status}'.format)
    next_activity = next(bot_status)
    logger.info(f"changing activity from {bot_status.__getstate__} to \'{next_activity}\'...")
    print(Yellow("[STATUS]:"), DarkGrey(f"\tchanging activity to "), Grey(f"\'{next_activity}\'"))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(next_activity))


#------------------------------------------------------------------------



@bot.event
async def on_ready():
    print(Yellow("[STATUS]:"), Blue(f"\t[{__name__}]"), f'\tWe have logged in as ', BrightYellow(f'{bot.user}'), Cyan(f'(ID: {bot.user.id})'))
    print(Yellow("[STATUS]:"), Blue(f"\t[{__name__}]"), f"\tStatus Cycle timer tick has been set to {Util.timetick} seconds")
    change_status.start()                #Q# video: Making a Discord Bot in Python (Part 3: Activity Status)
    print(Yellow("[STATUS]:"), Blue(f"\t[{__name__}]"), BrightGreen(f"\tReady!"))


@bot.command(name="dev_online", alias=["dev","do","running"])
async def dev_online(ctx):
    """See who's running BraxCord!"""
    devname = Auth.DEV_NAME
    await ctx.reply(f"The dev that's running me is {devname}!")



# ( I went ahead and moved your bot events over to Commands.py, Eli. I hope you don't mind, but it makes merging easier)

#PORTME
"""@bot.command(name='guilds', description="Displays the guilds a user shares with Brax")
async def display_shared_guilds(ctx, member:discord.Member): 
    user_id = member.id 
    guilds = await get_from_userguild(user_id) 

    if not guilds: 
        await ctx.send(f"User {member.name} does not have any guild-related records stored 👎") #Print to terminal
        return
    
    shared_guilds = [] #List to store shared guilds and iterate through for display 

    for guild in bot.guilds: #Fetch the guilds in memory 
        if guild.id in guilds: #If the guild id is also present in local guilds list 
            shared_guilds.append(guild.name) #add to the end of the shared guilds list 

    if not shared_guilds: #if not found in shared guilds,
       await ctx.send(f"User {member.name} does not have any shared guilds with Brax, or, the database has not been updated")
       return

    message = "🍅 Shared Guilds with Brax 🍅"
    for i, guild_name in enumerate(shared_guilds, start=1): 
        message += f"{i}. {guild_name}\n"
    
    await ctx.send(message)"""


# -----------------------------------------------------------------------------------------------------------




#Q# would ideally be eventually merged into the MyClient class
async def load():
    """
    Acts as MyClient()'s `async def on_ready(self)`.
    
    - Removes default !help
    - Loads cogs
    - awaits db.[TABLE_NAME].create_table()
    """
    bot.remove_command('help')  # removed to accommodate for the Help.py cog
    
    #for filename in os.listdir("./cogs"):
    #    if filename.endswith(".py"):
    #        extension = f"cogs.{filename[:-3]}"
    #        await bot.load_extension(extension)      # [:-3] is for string splicing
    #            #print(f"{filename[:-3]} is loaded")    # will be placed inside the cog
    #await bot.tree.sync(guild=MY_GUILD)#guild=discord.Object(id=Your guild id))
    print(Purple("\nLoading Cogs:"))
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            filename = file[:-3]
            try:
                await bot.load_extension(f"cogs.{filename}") #self.load
                print(Blue(f"- {filename} ✅ "))
            except:
                print(Blue(f"- {filename} ❌ "))

        # FOR COG DEBUGGING
        #if file == "Commands.py":
        #    filename = file[:-3]
        #    await bot.load_extension(f"cogs.{filename}")
    
    ####  HERE  ######
    await initialize_db()
    #await bot.db.bank.create_table()
    #await bot.db.inv.create_table()
    await bot.db.resp.create_table()
    
    print(Cyan("Created/modified tables successfully"))


# -----------------------------------------------------------------------------------


async def main():
    """Main function."""
    # create a directory
    await aiofiles.os.makedirs('logs', exist_ok=True)
    
    # LOGGING (https://medium.com/@thomaschaigneau.ai/building-and-launching-your-discord-bot-a-step-by-step-guide-f803f7943d33)
    # https://docs.python.org/3/library/logging.html#module-logging
    # https://discordpy.readthedocs.io/en/latest/logging.html
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    logging.getLogger('discord.http').setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename= 'logs/discord.log',      #f"{os.getenv('DATABASE_VOLUME')}/discord.log",
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  #32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    date_format = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', date_format, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info('Started')
    # END LOGGING
    
    async with bot:
        logger.info('running: main > _async with bot_')
        await load()
        print(Yellow("[STATUS]:"), Blue(f"\t[{__name__}]"), BrightGreen(f"\tCogs are done loading!"))
        await bot.start(Auth.TOKEN)   # replaces client.run(TOKEN)


# ----------------------------------------------------------

asyncio.run(main())
logger.info('Finished')

