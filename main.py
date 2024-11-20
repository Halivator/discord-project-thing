### BraxCord Discord Bot
# main.py
# Created: 11/11/24 ~ 5:21pm
# Last Updated: 11/11/24 ~ 5:21pm

#Q# NOTE: 11/11-Q: tutorial followed for initial code setup below:  (planning to remove some of the comment annotations at a later date)
# https://www.freecodecamp.org/news/create-a-discord-bot-with-python/

#############################################################################

from dotenv import load_dotenv
import discord 
from discord.ext import commands, tasks

from itertools import cycle     #Q# video: Making a Discord Bot in Python (Part 3: Activity Status)

import os           #Q# os library is only used to get the TOKEN from the .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


##client = discord.Client()           #Q# creates instance of connection to Discord  ## received error: Client.__init__() missing 1 required keyword-only argument: 'intents'


intents = discord.Intents.default()
# set particular Intents                        # https://discordpy.readthedocs.io/en/latest/api.html?highlight=client#intents
intents.message_content = True
client = discord.Client(intents=intents)        # https://stackoverflow.com/a/74331540


#Q# More about @client.events  :     https://discordpy.readthedocs.io/en/latest/api.html#discord.Client.event


#------------------------------------------------------------------------

#Q# video: Making a Discord Bot in Python (Part 3: Activity Status)
#------------------------------------------------------------------------
bot_status = cycle(["type in '___' for help", "Status One", "Status Two", "Status Three", "Status Four"])

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(bot_status)))


#------------------------------------------------------------------------






@client.event
async def on_ready():       #Q# - on_ready(), on_message() is an example of an event callback, aka when something happens
    print('We have logged in as {0.user}'.format(client))
    change_status.start()                #Q# video: Making a Discord Bot in Python (Part 3: Activity Status)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')




#client.run(os.getenv(TOKEN))      #Q# make sure that a .env file containing "TOKEN="{the_discord_bot_token}"" is in your project root directory
client.run(TOKEN)                   #Q# Solution found via: https://stackoverflow.com/a/63530919