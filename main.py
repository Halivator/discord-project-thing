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
#import mylib
import aiofiles
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


#client = discord.Client(intents=intents)        # https://stackoverflow.com/a/74331540

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
bot_status = cycle(["type in '___' for help", "Status One", "Status Two", "Status Three", "Status Four"])

@tasks.loop(seconds=timetick)
async def change_status():
    #print('{bot_status}'.format)
    next_activity = next(bot_status)
    logger.info(f"changing activity from {bot_status.__getstate__} to \'{next_activity}\'...")
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
#@bot.event
#async def on_message(message):
#    if message.author == bot.user:
#        return
#
#    if message.content.startswith('$hello'):
#        await message.channel.send('Hello!')
#    
#    if message.content.startswith('$gambling'):
#        #do gambling
#        await message.channel.send("Aw dang it!")
#    
#
#    await bot.process_commands(message)
#    print(message.content)


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
#@bot.tree.command(name="homie",description="tell me all of your commands and app commands")
#async def slash_command(interaction:discord.Interaction):
#    a = []
#    b = []
#    # Remove by value
#    #a.remove("banana")  
#
#    # Remove by index
#    #val = a.pop(1)
#    #print(val)
#    
#    for filename in os.listdir("./cogs"):
#        if filename.endswith(".py"):
#            namer = f"{filename[:-3]}"
#            cog = bot.get_cog(namer)
#            commands = cog.get_commands()
#            appcommands = cog.get_app_commands()
#            listeners = cog.get_listeners()
#            co = [c.name for c in commands]
#            ac = [a.name for a in appcommands]
#            li = [l.name for l in listeners]
#            cogresult = f"\ncog: {namer}.py\n commands: {co}\n app commands (use \' / \'): {ac}\n listeners: {li}\n------"
#            print(cogresult)
#            a.append(cogresult)
#    #temp = bot.tree.get_commands()  # guild = MY_GUILD, type=)
#    ##temp2 = bot.get_commands()
#    #for c in temp:
#    #    result = f"\n- ```{c.name}```"
#    #    b.append(result)
#    #ti = [c.name for c in temp]
#    c = f"Loaded from Cogs: {a}\nLoaded from command tree: {b}\n------"
#    
#    print(c)
#    await interaction.response.send_message(c)


# WORKS
@bot.tree.command(name="hello", description="Says hello!")
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message("Hello there!")

# WORKS
@bot.tree.command(name="cogchk", description="Checks the cog commands!")
async def cogchk(interaction: discord.Interaction):
    """Check the cog commands!"""
    cog = bot.get_cog('Ping')
    commands = cog.get_commands()
    result = [c.name for c in commands]
    print(result)
    await interaction.response.send_message(f"{result}")


# WORKS
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



# WORKS
@bot.tree.command()
@app_commands.describe(
    first_value='The first value you want to add something to',
    second_value='The value you want to add to the first value',
)
async def add(interaction: discord.Interaction, first_value: int, second_value: int):
    """Adds two numbers together."""
    await interaction.response.send_message(f'{first_value} + {second_value} = {first_value + second_value}')




"""
# The rename decorator allows us to change the display of the parameter on Discord.
# In this example, even though we use `text_to_send` in the code, the client will use `text` instead.
# Note that other decorators will still refer to it as `text_to_send` in the code.
@bot.tree.command()
@app_commands.rename(text_to_send='text')
@app_commands.describe(text_to_send='Text to send in the current channel')
async def send(interaction: discord.Interaction, text_to_send: str):
    ###""Sends the text into the current channel.""
    await interaction.response.send_message(text_to_send)
"""




#@bot.command(alias=['8ball', '8b', 'eightball', '8 ball'])
#async def magic_eightball(ctx, *, question=None):
#    #with open("responses.txt", "r") as f:        # "r" = read mode   
#    #    random_responses = f.readlines()                    # file is being treated as a list
#    #    response = random.choice(random_responses)
#    
#    if question is not None:
#        with open ('responses.txt', 'r',  encoding='utf-8') as f:
#            random_responses = f.readlines()
#            response = random.choice(random_responses)
#        
#            await ctx.send(f"The answer to \"{question}\" is this: {response}")
#    else:
#        await ctx.send('You did not ask a question.')
#    
    


#@bot.command(name='7ball')
#async def magic_sevenball(ctx, *, question):
#    
#    async with open("./responses.txt", 'r', encoding='utf-8') as f:        # "r" = read mode   
#        random_responses = f.readlines()                    # file is being treated as a list
#        response = random.choice(random_responses)
#        await response
#
#    await ctx.send(f"The answer to \"{question}\" is this: {response}")


#WORKS
@bot.tree.command()
async def get_username(interaction: discord.Interaction):
    """Gets the username of the user who invoked the command."""
    logger.info('Doing something')
    username = interaction.user.name
    julien = interaction.user.nick
    feets = interaction.user.joined_at
    await interaction.response.send_message(f'Your username is {username}. nickname: {julien}. joined at: {feets}')











async def load():
    bot.remove_command('help')
    
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            extension = f"cogs.{filename[:-3]}"
            await bot.load_extension(extension)      # [:-3] is for string splicing
                #print(f"{filename[:-3]} is loaded")    # will be placed inside the cog
    #await bot.tree.sync(guild=MY_GUILD)#guild=discord.Object(id=Your guild id))


async def main():
    """Main function."""
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
        #bot.setup_hook = load()
        await load()
        #await on_ready(bot)
        await bot.start(TOKEN)   # replaces client.run(TOKEN)
        






asyncio.run(main())
logger.info('Finished')


#client.run(os.getenv(TOKEN))      #Q# make sure that a .env file containing "TOKEN="{the_discord_bot_token}"" is in your project root directory
#client.run(TOKEN)                   #Q# Solution found via: https://stackoverflow.com/a/63530919