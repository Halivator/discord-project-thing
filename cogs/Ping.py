# Ping.py
# Quinn
# Uses tutorial: Making A Discord Bot In Python (Part 4: Cogs)
# https://www.youtube.com/watch?v=hxsGrMijgUA&list=PLwqYQaS6jxfk_NCetUOyNRDGAf9_kU90n&index=4

from base import Util

import discord
from discord.ext import commands
from discord     import app_commands
import asyncio

class Ping(commands.Cog):
    """
    This one has commands to check connectivity and responses
    """
    
    def __init__(self, bot):
        self.bot = bot
        
    
    @commands.Cog.listener()    # events use this decorator
    async def on_ready(self):
        #await self.bot.tree.sync()
        print(f"{__name__} is ready!")
        
        
    #@client.tree.command()
    
    # SLASH COMMAND ONLY
    #@app_commands.command(description="Sends the bot's latency in milliseconds (ms.)")
    #async def ping(self, interaction: discord.Interaction): #, text_to_send: str):
    #    bot_latency = round(self.bot.latency * 1000)
    #    await interaction.response.send_message(f"Pong! {bot_latency} ms.") # {text_to_send}")
    
    
    # HYBRID COMMAND (PREFIXED COMMAND AND SLASH COMMAND)
    @commands.hybrid_command(name="ping", description="Sends the bot's latency in milliseconds (ms.)", with_app_command=True)
    async def ping(self, ctx: commands.Context): #interaction: discord.Interaction): #, text_to_send: str):
        #bot_latency = round(self.bot.latency * 1000)
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)} ms.")
    
    # PREFIXED COMMAND ONLY
    @commands.command(name="pung", description="Sends the bot's latency in milliseconds (ms.)")
    async def pung(self, ctx): #interaction: discord.Interaction): #, text_to_send: str):
        #bot_latency = round(self.bot.latency * 1000)
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)} ms.")
    
    # ------------------------------------
    
    @commands.hybrid_command(name="pong", description="Testing a condition with hybrid command", with_app_command=True)
    async def pong(self, ctx: commands.Context, message: str = None): #interaction: discord.Interaction): #, text_to_send: str):
        #if message is not None:
        #    message = message
        if message == 'test': 
            message = 'https://tenor.com/bFrLl.gif'
        elif message is None: 
            message = 'theres no message here...' 
        await ctx.defer()
        await asyncio.sleep(5)
        await ctx.send(message)
        #await ctx.send_message(message) # {text_to_send}")


    #@commands.hybrid_command(name="echo", description="Echoes a message", with_app_command=True)
    #@app_commands.describe(message="The message to echo")
    #async def echo(self, ctx: commands.Context, *, message: str):
    #    await ctx.send(message)

    #@commands.command()
    #async def oldschool(self, ctx, *, message: str):
    #    await ctx.send(message)
#
    #@commands.command()
    #async def oldie(self, ctx):
    #    await ctx.send("this is an oldie")



    @commands.hybrid_command(name="get_tickrate", alias=['tr','tick','tick rate', 'clock speed'] , description="Get the tick rate back in seconds", with_app_command=True)
    async def get_tickrate(self, ctx: commands.Context): #interaction: discord.Interaction): #, text_to_send: str):
        await ctx.send(f'The tick rate is set to {Util.timetick} seconds!')
        #await ctx.send_message(message) # {text_to_send}")

    @commands.hybrid_command(name="set_tickrate", alias=['str','st','s_t', 'setrate'], description="Sets the tick rate back in seconds", with_app_command=True)
    async def tickrate(self, ctx: commands.Context, speed: int): #interaction: discord.Interaction): #, text_to_send: str):
        message = ''
        is_valid = True
        if speed < 0:
            message = "Error: You can't set a speed less than 0!"
            is_valid = False
        elif speed == 69: 
            message = ' (nice!)'
            Util.timetick = speed;
        else:
            Util.timetick = speed;
        await ctx.defer()
        await asyncio.sleep(5)
        if is_valid == True:
            await ctx.send(f'The tick rate has been set to {Util.timetick} sec.{message}')
        else:
            await ctx.send(f'{message}')
        #await ctx.send_message(message) # {text_to_send}")



async def setup(bot):
    await bot.add_cog(Ping(bot))      #add_cog(NAME_OF_CLASS(client))   #case sensitive