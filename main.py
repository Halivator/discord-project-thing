### BraxCord Discord Bot
# main.py
# Created: 11/11/24 ~ 5:21pm
# Last Updated: 11/11/24 ~ 5:21pm

#Q# NOTE: 11/11-Q: tutorial followed for initial code setup below:  (planning to remove some of the comment annotations at a later date)
# https://www.freecodecamp.org/news/create-a-discord-bot-with-python/

#############################################################################

from dotenv import load_dotenv
import discord
import os           #Q# os library is only used to get the TOKEN from the .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


##client = discord.Client()           #Q# creates instance of connection to Discord  ## received error: Client.__init__() missing 1 required keyword-only argument: 'intents'


intents = discord.Intents.default()
# set particular Intents                        # https://discordpy.readthedocs.io/en/latest/api.html?highlight=client#intents
intents.message_content = True
client = discord.Client(intents=intents)        # https://stackoverflow.com/a/74331540


#Q# More about @client.events  :     https://discordpy.readthedocs.io/en/latest/api.html#discord.Client.event






@client.event
async def on_ready():       #Q# - on_ready(), on_message() is an example of an event callback, aka when something happens
    print('We have logged in as {0.user}'.format(client))



@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')




