### BraxCord Discord Bot
# main.py
# Created: 11/11/24 ~ 5:21pm
# Last Updated: 12/07/24 ~ 12:27 AM

#Q# NOTE: 11/11-Q: tutorial followed for initial code setup below:  (planning to remove some of the comment annotations at a later date)
# https://www.freecodecamp.org/news/create-a-discord-bot-with-python/
#############################################################################

from dotenv import load_dotenv
import discord 
from discord import app_commands
from discord.ext import commands, tasks

from itertools import cycle

import random
import aiofiles, aiofiles.os
import logging
import logging.handlers
import os #Q# os library is only used to get the TOKEN from the .env file
import asyncio
from data_models import UserGuild, Responses, Wallet, Base, async_session, initialize_db 
from database_operations import add_to_userguild, get_from_userguild, delete_from_userguild, create_user_wallet, get_user_wallet, update_user_wallet, delete_user_wallet, WalletModel

load_dotenv()
logger = logging.getLogger(__name__)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

TOKEN = os.getenv("DISCORD_TOKEN")
APP_ID = os.getenv("APPLICATION_ID")
MY_GUILD = discord.Object(id=1182049728058380409)

#slash commands instead of old! commands
class MyClient(commands.Bot):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(command_prefix=['!'],intents= intents) #intents)

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
intents.guilds = True
intents.members = True

#client = discord.Client(intents=intents)        # https://stackoverflow.com/a/74331540

bot = MyClient(intents=intents) #command_prefix=['$!'],      # https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html#ext-commands-commands
#bot.application_id(APP_ID)

#tree = app_commands.CommandTree(bot)
# HERE https://stackoverflow.com/questions/71165431/how-do-i-make-a-working-slash-command-in-discord-py

#Q# More about @client.events  :     https://discordpy.readthedocs.io/en/latest/api.html#discord.Client.event

timetick = 15
#------------------------------------------------------------------------
#Q# video: Making a Discord Bot in Python (Part 3: Activity Status)
#------------------------------------------------------------------------
bot_status = cycle(["Throwing tomatoes (!help)", "Shut up, nerd (!help)", "Cyberbulling Children (!help)", "Taking your lunch money! (!help)", "Dev Online: Eli"])

@tasks.loop(seconds=timetick)
async def change_status():
    #print('{bot_status}'.format)
    next_activity = next(bot_status)
    print(f"changing activity now to \'{next_activity}\'")
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(next_activity))

#-------------------------------------------------------------------------------------------
@bot.event
async def on_ready():       #Q# - on_ready(), on_message() is an example of an event callback, aka when something happens
    print('We have logged in as {0.user}'.format(bot))
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print(f"Cycle timer tick has been set to {timetick}")
    change_status.start()                #Q# video: Making a Discord Bot in Python (Part 3: Activity Status)
##    await bot.tree.sync(guild=MY_GUILD) #guild=discord.Object(id=Your guild id))
    print("Ready!")
    #await client.tree.sync() #client.tree.sync()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    await bot.process_commands(message)
    print(message.content)

@bot.event
#pre-defined function by discord to run when a bot is added to a server
#when bot is added to server, populate the userguild table with members 
async def on_guild_join(guild: discord.Guild): 
    for member in guild.members: #E - for each of the members in the guild 
        if member.bot == True: #E - if the member is a BOT, drop down to next block of code
            continue 
        try: 
            await add_to_userguild(
                user_id=member.id, 
                guild_id=guild.id, 
                guild_name=guild.name
            )
            print(f"Added user of {member.name} with ID {member.id} to UserGuild table for Guild: {guild.name}") #For logging/testing
        except Exception: 
            print(f"Could not add user {member.name} to UserGuild table") #For logging/testing'''

@bot.event
#When the bot has been removed from the server, get rid of data stored by the bot
async def on_guild_remove(guild: discord.Guild): 
    removal_count = await delete_from_userguild(guild_id=guild.id) #Remove from UserGuild table where guild_ids match

    if removal_count > 0: 
        print(f"Successfully removed records for {guild.name} : {guild.id} from UserGuilds") ##For logging & testing
    else: 
        print(f"Error removing records for {guild.name} : {guild.id} from UserGuilds")

@bot.event 
async def on_member_join(member: discord.Member): 
    """When a member joins the server, create their wallet (utilizes create_user_wallet)"""
    wallet_created = await create_user_wallet(user_id=member.id, initial_balance=0, starting_number_of_tomatoes=0)
    if wallet_created: 
        print(f"The wallet was successfully created for {member.name} : {member.id}") #Print to terminal, since this happens by default, user does not need to see this message
    else: 
        print(f"There was an error creating the wallet for {member.name} : {member.id}, or, a wallet already exists for this user")
     
@bot.event 
async def on_member_remove(member: discord.Member): 
    """When a member leaves the server, remove their wallet (utilizes delete_user_wallet)"""
    wallet_deleted = await delete_user_wallet(user_id=member.id)
    if wallet_deleted: 
        print(f"The wallet for user {member.name} : {member.id} has been successfully removed.")
    else: 
        print(f"The wallet for user {member.name} could not be deleted, or was not found.")
       
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


#E# - https://chatgpt.com/share/6753dcab-f708-8007-ad20-126bc14bcd10 - Chatlog for help debugging and getting resources on using the context(ctx) object
@bot.command(name='wallet', description="Allow user's to view their wallet's contents") ##Utilizes get_user_wallet and create_user_wallet operations
async def wallet(ctx):
    """Command to display balance and inventory of a user's wallet"""
    """If a user is existing in the server but doesn't have a wallet, create one for them"""
    ##Attributes to create a wallet and address user
    user_id = ctx.author.id 
    name = ctx.author.name 

    #Retrieval of data from WALLETS data table 
    wallet_contents = await get_user_wallet(user_id)

    if wallet_contents: #If the wallet exists, display contents and balance
        balance = wallet_contents.balance 
        tomatoes = wallet_contents.number_of_tomatoes
        await ctx.send(f"💸 {name}, your wallet balance is ${balance}\n You currently have {tomatoes} tomatoes 🍅")
    else: #Otherwise, the wallet doesn't exist, so create one for the user and add it to the database
        initial_balance = 0
        initial_tomatoes = 0
        await create_user_wallet(user_id, initial_balance, initial_tomatoes)
        await ctx.send(f"💯 {name}, your wallet has successfully been created with a balance of ${initial_balance} and inventory of {initial_tomatoes} tomatoes")


#PORTME
@bot.command(name='update_balance', description="Allows server administrators to change balance of a user's wallet")
@commands.has_permissions(administrator=True) #Only allow server admins to interact with this command 
async def update_wallet_balance(ctx, member: discord.Member, new_balance:int): 
    """Update a user's wallet balance - for administrators only"""
    try: 
        updated_wallet = WalletModel(balance=new_balance, number_of_tomatoes=None)

        await update_user_wallet(user_id = member.id, updatedWallet=updated_wallet)
        await ctx.send(f"Successfully updated {member.name}'s balance to {new_balance} 💸") #Success message when user's balance has been updated to db 
    except Exception as ex: 
        await ctx.send(f"An error occurred while trying to update {member.name}'s balance: {str(ex)}") #otherwise display error message to discord

#PORTME 
@bot.command(name='update_tomatoes', description="Allow server administrators to change the number of tomatoes a user has in their wallet")
@commands.has_permissions(administrator=True)
async def update_user_tomatoes(ctx, member:discord.Member, new_tomato_balance:int):
    """Update the number of tomatoes a user has in their inventory - for administrators only"""
    try: 
        updated_wallet = WalletModel(balance=None, number_of_tomatoes=new_tomato_balance)

        await update_user_wallet(user_id=member.id, updatedWallet=updated_wallet)
        await ctx.send(f"Successfully updated {member.name}'s tomato balance to {new_tomato_balance} 🍅") #Success message when user's tomato count has been updated to db
    except Exception as ex: 
        await ctx.send(f"An error occurred while trying to update {member.name}'s wallet: {str(ex)}") #Otherwise display error message to discord

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            extension = f"cogs.{filename[:-3]}"
            await bot.load_extension(extension)      # [:-3] is for string splicing
                #print(f"{filename[:-3]} is loaded")    # will be placed inside the cog
    #await bot.tree.sync(guild=MY_GUILD)#guild=discord.Object(id=Your guild id))

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
        await initialize_db()
        #bot.setup_hook = load()
        await load()
        #await on_ready(bot)
        await bot.start(TOKEN)   # replaces client.run(TOKEN)

asyncio.run(main())
logger.info('Finished')