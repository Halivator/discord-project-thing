import discord
from discord.ext import commands
import asyncio
import random
import os           #Q# os library is only used to get the TOKEN from the .env file


class Eightball(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()    # events use this decorator
    async def on_ready(self):
        print("eightball.py is ready!")
    
    #@commands.command()          # commands use this decorator
    #async def eightball(self, ctx):                      # when working with a cog, `self` goes before anything else in your command
    #    bot_latency = round(self.client.latency * 1000)
#
    #    await ctx.send(f"Pong! {bot_latency} ms.")
    
    @commands.command()          # commands use this decorator
    async def eightball(self, ctx, *, question):                      # when working with a cog, `self` goes before anything else in your command
        with open("responses.txt", "r") as f:        # "r" = read mode   
            random_responses = f.readlines()                    # file is being treated as a list
            response = random.choice(random_responses)
    
        await ctx.send(response)
    
        
async def setup(client):
    await client.add_cog(Eightball(client))      #add_cog(NAME_OF_CLASS(client))   #case sensitive