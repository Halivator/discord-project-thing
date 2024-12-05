### BraxCord Discord Bot
# main.py
# Created: 11/11/24 ~ 5:21pm
# Last Updated: 12/01/24 ~ 5:21pm

#Q# NOTE: 11/11-Q: tutorial followed for initial code setup below:  (planning to remove some of the comment annotations at a later date)
# https://www.freecodecamp.org/news/create-a-discord-bot-with-python/

#############################################################################

import aiofiles.os
from dotenv import load_dotenv
import discord 
from discord import app_commands
from discord.ext import commands, tasks
import discord
from discord.ext import commands
from discord.ui import Button, View

from itertools import cycle
#import mylib
import aiofiles, aiofiles.os
import logging
import logging.handlers
import asyncio
import random
import os           #Q# os library is only used to get the TOKEN from the .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

APP_ID = os.getenv("APPLICATION_ID")
#APPLICATION_ID="1305627246022627359"
T_GUILD = os.getenv("TEST_GUILD")
t_id = int(T_GUILD)
MY_GUILD = discord.Object(id=t_id)

logger = logging.getLogger(__name__)

#slash commands instead of old! commands ----------


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

class MyClient(commands.Bot):
    def __init__(self, command_prefix, log_handler, log_level, *, intents: discord.Intents):
        super().__init__(command_prefix=command_prefix, log_handler=log_handler, log_level=log_level, intents= intents) #intents)

        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.

        #self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

# set particular Intents                        # https://discordpy.readthedocs.io/en/latest/api.html?highlight=client#intents
intents = discord.Intents.default() #all() #.default()
intents.message_content = True
bot = MyClient(command_prefix='!',log_handler=handler,log_level=logging.DEBUG,intents=intents) #command_prefix=['$!'],      # https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html#ext-commands-commands

##client = discord.Client()           #Q# creates instance of connection to Discord  ## received error: Client.__init__() missing 1 required keyword-only argument: 'intents'


#intents = discord.Intents.default()
## set particular Intents                        # https://discordpy.readthedocs.io/en/latest/api.html?highlight=client#intents
#intents.message_content = True
#client = discord.Client(intents=intents)        # https://stackoverflow.com/a/74331540


#Q# More about @client.events  :     https://discordpy.readthedocs.io/en/latest/api.html#discord.Client.event

@bot.event
async def on_ready():       #Q# - on_ready(), on_message() is an example of an event callback, aka when something happens
    print('We have logged in as {0.user}'.format(bot))
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    #print(f"Cycle timer tick has been set to {timetick}")
    print("Ready!")



@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    await bot.process_commands(message)
    print(message.content)







async def load():
    """Loads the extensions in the cogs/ folder"""
    bot.remove_command('help')
    
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            extension = f"cogs.{filename[:-3]}"
            await bot.load_extension(extension)


async def main():
    """Main function."""
    # LOGGING (https://medium.com/@thomaschaigneau.ai/building-and-launching-your-discord-bot-a-step-by-step-guide-f803f7943d33)
    # https://docs.python.org/3/library/logging.html#module-logging
    # https://discordpy.readthedocs.io/en/latest/logging.html
    await aiofiles.os.makedirs('logs', exist_ok=True)
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
        await bot.start(TOKEN)   # replaces client.run(TOKEN)



#client.run(os.getenv(TOKEN))      #Q# make sure that a .env file containing "TOKEN="{the_discord_bot_token}"" is in your project root directory
#bot.run(TOKEN)                   #Q# Solution found via: https://stackoverflow.com/a/63530919


asyncio.run(main())
logger.info(f'---------\nFinished\n----------')
