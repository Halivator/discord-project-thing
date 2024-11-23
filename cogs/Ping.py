# Ping.py
# Quinn
# Uses tutorial: Making A Discord Bot In Python (Part 4: Cogs)
# https://www.youtube.com/watch?v=hxsGrMijgUA&list=PLwqYQaS6jxfk_NCetUOyNRDGAf9_kU90n&index=4

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
    
    @app_commands.command(description="Sends the bot's latency in milliseconds (ms.)")
    async def ping(self, interaction: discord.Interaction): #, text_to_send: str):
        bot_latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"Pong! {bot_latency} ms.") # {text_to_send}")
    
    #@commands.hybrid_command(name="ping", description="Sends the bot's latency in milliseconds (ms.)", with_app_command=True)
    #async def ping(self, ctx: commands.Context): #interaction: discord.Interaction): #, text_to_send: str):
    #    #bot_latency = round(self.bot.latency * 1000)
    #    await ctx.send_message(f"Pong! {round(self.bot.latency * 1000)} ms.")
        
    
    @commands.hybrid_command(name="pong", description="Testing a condition with hybrid command", with_app_command=True)
    async def pong(self, ctx: commands.Context, message: str = None): #interaction: discord.Interaction): #, text_to_send: str):
        if message is not None:
            message = message
        elif message is None:
            message = str("theres no message here...")
        await ctx.defer()
        await asyncio.sleep(5)
        await ctx.send_message(message) # {text_to_send}")


    @commands.hybrid_command(name="echo", description="Echoes a message", with_app_command=True)
    @app_commands.describe(message="The message to echo")
    async def echo(self, ctx: commands.Context, *, message: str):
        await ctx.send(message)

    @commands.command()
    async def oldschool(self, ctx, *, message: str):
        await ctx.send(message)

    @commands.command()
    async def oldie(self, ctx):
        await ctx.send("this is an oldie")


async def setup(bot):
    await bot.add_cog(Ping(bot))      #add_cog(NAME_OF_CLASS(client))   #case sensitive