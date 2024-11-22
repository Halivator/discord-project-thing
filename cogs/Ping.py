# Ping.py
# Quinn
# Uses tutorial: Making A Discord Bot In Python (Part 4: Cogs)
# https://www.youtube.com/watch?v=hxsGrMijgUA&list=PLwqYQaS6jxfk_NCetUOyNRDGAf9_kU90n&index=4

import discord
from discord.ext import commands
from discord     import app_commands

class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()    # events use this decorator
    async def on_ready(self):
        print("Ping.py is ready!")
    


    @app_commands.command(description="Ping Pong")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong")
    



async def setup(client):
    await client.add_cog(Ping(client))      #add_cog(NAME_OF_CLASS(client))   #case sensitive