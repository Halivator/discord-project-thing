# Ping.py
# Quinn
# Uses tutorial: Making A Discord Bot In Python (Part 4: Cogs)
# https://www.youtube.com/watch?v=hxsGrMijgUA&list=PLwqYQaS6jxfk_NCetUOyNRDGAf9_kU90n&index=4

import discord
from discord.ext import commands
from discord     import app_commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()    # events use this decorator
    async def on_ready(self):
        print("Ping.py is ready!")
        
        
    #@client.tree.command()
    
    @app_commands.command(description="Ping Pong")
    async def ping(self, interaction: discord.Interaction): #, text_to_send: str):
        await interaction.response.send_message(f"Pong!") # {text_to_send}")
    
    @commands.hybrid_command(name="pong", with_app_command=True)
    async def pong(self, interaction: discord.Interaction): #, text_to_send: str):
        await interaction.response.send_message(f"Ping!") # {text_to_send}")


    @commands.hybrid_command(name="echo", description="Echoes a message")
    @app_commands.describe(message="The message to echo")
    async def echo(self, ctx: commands.Context, message: str):
        await ctx.send(message)



async def setup(bot):
    await bot.add_cog(Ping(bot))      #add_cog(NAME_OF_CLASS(client))   #case sensitive