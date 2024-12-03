### BraxCord Discord Bot
# main.py
# Created: 11/11/24 ~ 5:21pm
# Last Updated: 12/01/24 ~ 7:34pm

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
from data_models import User, Guild, UserGuild, Responses, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

APP_ID = os.getenv("APPLICATION_ID")
#APPLICATION_ID="1305627246022627359"

MY_GUILD = discord.Object(id=1182049728058380409)

#E Database Setup - for loading database into project
engine = create_engine("sqlite:///Bot.db") #E - will load in if the db file is in the same folder as project
Base.metadata.create_all(engine)

#slash commands instead of old! commands
class MyClient(commands.Bot):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(command_prefix=['$!'],intents= intents) #intents)

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


intents = discord.Intents.default() #all() #.default()
# set particular Intents                        # https://discordpy.readthedocs.io/en/latest/api.html?highlight=client#intents
intents.message_content = True
intents.presences = True

#client = discord.Client(intents=intents)        # https://stackoverflow.com/a/74331540

bot = MyClient(intents=intents) #command_prefix=['$!'],      # https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html#ext-commands-commands
#bot.application_id(APP_ID)

#tree = app_commands.CommandTree(bot)
#
#
# HERE https://stackoverflow.com/questions/71165431/how-do-i-make-a-working-slash-command-in-discord-py
#

#Q# More about @client.events  :     https://discordpy.readthedocs.io/en/latest/api.html#discord.Client.event

timetick = 15

#------------------------------------------------------------------------
#Q# video: Making a Discord Bot in Python (Part 3: Activity Status)
#------------------------------------------------------------------------
bot_status = cycle(["type in '!help' for help", "throwing LOTS of tomatoes", "stealing your lunch money", "Status Three", "Status Four"])

@tasks.loop(seconds=timetick)
async def change_status():
    #print('{bot_status}'.format)
    next_activity = next(bot_status)
    print(f"changing activity now to \'{next_activity}\'")
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(next_activity))


#------------------------------------------------------------------------

@bot.event
async def on_ready():       #Q# - on_ready(), on_message() is an example of an event callback, aka when something happens
    print('We have logged in as {0.user}'.format(bot))
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print(f"Cycle timer tick has been set to {timetick}")
    change_status.start()                #Q# video: Making a Discord Bot in Python (Part 3: Activity Status)
##    await bot.tree.sync(guild=MY_GUILD) #guild=discord.Object(id=Your guild id))
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
    """Says hello!"""
    await interaction.response.send_message("Hello there!")


@bot.tree.command(name="cogchk", description="Checks the cog commands!")
async def cogchk(interaction: discord.Interaction):
    """Check the cog commands!"""
    cog = bot.get_cog('Ping')
    commands = cog.get_commands()
    result = [c.name for c in commands]
    print(result)
    await interaction.response.send_message(f"{result}")



@bot.tree.command(name="cogchk2", description="Checks the cog commands! Again! Also with app_commands")
async def cogchk2(interaction: discord.Interaction):
    """Check the cog commands!"""
    cog = bot.get_cog('Ping')
    commie = cog.get_app_commands()
    commands = cog.get_commands()
    result = [c.name for c in commands]
    result2 = [a.name for a in commie]
    print(f"commands: {result} \n app commands (use \'/\'): {result2}")
    await interaction.response.send_message(f"commands: {result} \n app commands (use \'\\\'): {result2}")

@bot.tree.command()
@app_commands.describe(
    first_value='The first value you want to add something to',
    second_value='The value you want to add to the first value',
)
async def add(interaction: discord.Interaction, first_value: int, second_value: int):
    """Adds two numbers together."""
    await interaction.response.send_message(f'{first_value} + {second_value} = {first_value + second_value}')


# The rename decorator allows us to change the display of the parameter on Discord.
# In this example, even though we use `text_to_send` in the code, the client will use `text` instead.
# Note that other decorators will still refer to it as `text_to_send` in the code.
@bot.tree.command()
@app_commands.rename(text_to_send='text')
@app_commands.describe(text_to_send='Text to send in the current channel')
async def send(interaction: discord.Interaction, text_to_send: str):
    """Sends the text into the current channel."""
    await interaction.response.send_message(text_to_send)



@bot.tree.command(name="other_8ball", description="Says hello!")
async def other_magic_eightball(interaction: discord.Interaction, question: str):
    with open(".responses.txt", "r") as f:        # "r" = read mode   
        random_responses = f.readlines()                    # file is being treated as a list
        response = random.choice(random_responses)
    
    await interaction.response.send_message(f"The answer to \"{question}\" is this: {response}")



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


#client.run(os.getenv(TOKEN))      #Q# make sure that a .env file containing "TOKEN="{the_discord_bot_token}"" is in your project root directory
#client.run(TOKEN)                   #Q# Solution found via: https://stackoverflow.com/a/63530919