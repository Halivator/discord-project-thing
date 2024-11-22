### BraxCord Discord Bot
# main.py
# Created: 11/11/24 ~ 5:21pm
# Last Updated: 11/11/24 ~ 5:21pm

#Q# NOTE: 11/11-Q: tutorial followed for initial code setup below:  (planning to remove some of the comment annotations at a later date)
# https://www.freecodecamp.org/news/create-a-discord-bot-with-python/

#############################################################################

from dotenv import load_dotenv
import discord 
from discord import app_commands
from discord.ext import commands, tasks

from itertools import cycle

import asyncio
import random
import os           #Q# os library is only used to get the TOKEN from the .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

APP_ID = os.getenv("APPLICATION_ID")
#APPLICATION_ID="1305627246022627359"

MY_GUILD = discord.Object(id=1182049728058380409)


#slash commands instead of old! commands





intents = discord.Intents.default() #all() #.default()
# set particular Intents                        # https://discordpy.readthedocs.io/en/latest/api.html?highlight=client#intents
intents.message_content = True


#client = discord.Client(intents=intents)        # https://stackoverflow.com/a/74331540

bot = commands.Bot(command_prefix='$', intents=intents)     # https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html#ext-commands-commands
#bot.application_id(APP_ID)

#tree = app_commands.CommandTree(bot)
#
#
# HERE https://stackoverflow.com/questions/71165431/how-do-i-make-a-working-slash-command-in-discord-py
#

#Q# More about @client.events  :     https://discordpy.readthedocs.io/en/latest/api.html#discord.Client.event


#------------------------------------------------------------------------

#Q# video: Making a Discord Bot in Python (Part 3: Activity Status)
#------------------------------------------------------------------------
bot_status = cycle(["type in '___' for help", "Status One", "Status Two", "Status Three", "Status Four"])

@tasks.loop(seconds=5)
async def change_status():
    print(f"activity")
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(next(bot_status)))


#------------------------------------------------------------------------






@bot.event
async def on_ready():       #Q# - on_ready(), on_message() is an example of an event callback, aka when something happens
    print('We have logged in as {0.user}'.format(bot))
    change_status.start()                #Q# video: Making a Discord Bot in Python (Part 3: Activity Status)
    await bot.tree.sync(guild=MY_GUILD) #guild=discord.Object(id=Your guild id))
    print("Ready!")
    #await client.tree.sync() #client.tree.sync()


#@client.event
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    await bot.process_commands(message)
    print(message.content)


#@bot.event
#async def on_message(message):
#    await bot.process_commands(message)
#    print(message.content)







# Add the guild ids in which the slash command will appear.
# If it should be in all, remove the argument, but note that
# it will take some time (up to an hour) to register the
# command if it's for all guilds.
#@tree.command(
#    name="BraxHello",
#    description="My first application Command",
#    guild=MY_GUILD #discord.Object(MY_GUILD)
#)
#async def first_command(interaction: discord.Interaction):
#    await interaction.response.send_message("Hello! I am BraxCord")





# https://dev.to/mannu/4slash-commands-in-discordpy-ofl
##```python
@bot.tree.command(name="mannu",description="Mannu is a good boy")
async def slash_command(interaction:discord.Interaction):
    await interaction.response.send_message("Hello World!")


@bot.tree.command(name="hello", description="Says hello!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello there!")

@commands.command(name='8ball')
async def magic_eightball(ctx, *, question):
    with open("discord-project-thing/responses.txt", "r") as f:        # "r" = read mode   
        random_responses = f.readlines()                    # file is being treated as a list
        response = random.choice(random_responses)
    
    await ctx.send(response)


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            extension = f"cogs.{filename[:-3]}"
            await bot.load_extension(extension)      # [:-3] is for string splicing
                #print(f"{filename[:-3]} is loaded")    # will be placed inside the cog
    #await bot.tree.sync(guild=MY_GUILD)#guild=discord.Object(id=Your guild id))


async def main():
    async with bot:
        #bot.setup_hook = load()
        await load()
        #await on_ready(bot)
        await bot.start(TOKEN)   # replaces client.run(TOKEN)
        



asyncio.run(main())



#client.run(os.getenv(TOKEN))      #Q# make sure that a .env file containing "TOKEN="{the_discord_bot_token}"" is in your project root directory
#client.run(TOKEN)                   #Q# Solution found via: https://stackoverflow.com/a/63530919