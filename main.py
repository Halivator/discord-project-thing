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
import discord
from discord.ext import commands
from discord.ui import Button, View

from itertools import cycle
#import mylib
#import aiofiles
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

@bot.command(name="market")
async def market(ctx):
    # Create an embed
    embed = discord.Embed(
        title="Market Actions",
        description="Choose what you want to do in the market:",
        color=discord.Color.blue()
    )
    embed.add_field(name="Buy", value="Purchase items from the market.", inline=False)
    embed.add_field(name="Sell", value="Sell your items in the market.", inline=False)
    embed.set_footer(text="Use the buttons below to proceed.")

    # Create two buttons
    button1 = Button(label="Buy", style=discord.ButtonStyle.green)
    button2 = Button(label="Sell", style=discord.ButtonStyle.red)

    # Define what happens when the buttons are clicked
    async def button1_callback(interaction):
        await interaction.response.send_message("You clicked the Buy button!", ephemeral=True)

    async def button2_callback(interaction):
        await interaction.response.send_message("You clicked the Sell button!", ephemeral=True)

    # Assign the callback to the buttons
    button1.callback = button1_callback
    button2.callback = button2_callback

    # Create a View to hold the buttons
    view = View()
    view.add_item(button1)
    view.add_item(button2)

    # Send the message with the embed and buttons
    await ctx.send(embed=embed, view=view)

#client.run(os.getenv(TOKEN))      #Q# make sure that a .env file containing "TOKEN="{the_discord_bot_token}"" is in your project root directory
client.run(TOKEN)                   #Q# Solution found via: https://stackoverflow.com/a/63530919