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
#import mylib
import aiofiles, aiofiles.os
import logging
import logging.handlers
import asyncio
#import random
from pycolorise.colors import *
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
bot = MyClient(command_prefix=f'{Auth.COMMAND_PREFIX}',log_handler=handler,log_level=logging.DEBUG,intents=intents) #command_prefix=['$!'],      # https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html#ext-commands-commands

#------------------------------------------------------------------------
#Q# video: Making a Discord Bot in Python (Part 3: Activity Status)
#------------------------------------------------------------------------
status_phrases = [
    f"try {Auth.COMMAND_PREFIX}help",
    f"Throwing tomatoes ({Auth.COMMAND_PREFIX}help)",
    f"Shut up, nerd ({Auth.COMMAND_PREFIX}help)",
    f"Cyberbullying Children ({Auth.COMMAND_PREFIX}help)",
    f"there's no //j here! ({Auth.COMMAND_PREFIX}help)",
    ]
"""List of statuses to cycle through"""

if Auth.DEV_NAME is not None: status_phrases.append(f"developer online: {Auth.DEV_NAME} ({Auth.COMMAND_PREFIX}help)")

bot_status = cycle(status_phrases)

@tasks.loop(seconds = Util.timetick)
async def change_status():
    #print('{bot_status}'.format)
    next_activity = next(bot_status)
    logger.info(f"changing activity from {bot_status.__getstate__} to \'{next_activity}\'...")
    print(f"changing activity now to \'{next_activity}\'")
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(next_activity))


#------------------------------------------------------------------------



@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print(f"Cycle timer tick has been set to {Util.timetick}")
    change_status.start()                #Q# video: Making a Discord Bot in Python (Part 3: Activity Status)
    print("Ready!")


@bot.command(name="dev_online", alias=["dev","do","running"])
async def dev_online(ctx):
    """See who's running BraxCord!"""
    devname = Auth.DEV_NAME
    await ctx.reply(f"The dev that's running me is {devname}!")


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


#E# - https://chatgpt.com/share/6753dcab-f708-8007-ad20-126bc14bcd10 - Chatlog for help debugging and getting resources on using the context(ctx) object
@bot.command(name='wallet', description="Allow user's to view their wallet's contents")
async def wallet(ctx):
    """Command to display balance and inventory of a user's wallet (utilizes get_user_wallet & create_user_wallet)"""
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


#TODO: Flesh out this bot command
@bot.command(name='change_balance', description="Allows server admins to change balance of a user's wallet")
@commands.has_permissions(administrator=True) #Only allow server admins to interact with this command 
async def update_wallet_balance(ctx): 
    """Command to allow server admins to change a user's balance"""
    pass



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
        await bot.start(Auth.TOKEN)   # replaces client.run(TOKEN)


# ----------------------------------------------------------

asyncio.run(main())
logger.info('Finished')

