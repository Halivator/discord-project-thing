import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import random
import aiofiles
import os           #Q# os library is only used to get the TOKEN from the .env file


class Eightball(commands.Cog):
    """
    Lets go gambling!
    AW DANG IT
    AW DANG IT
    AW DANG IT
    AW DANG IT
    """
    
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()    # events use this decorator
    async def on_ready(self):
        print("Eightball.py is ready!")
    
    #@commands.command()          # commands use this decorator
    #async def eightball(self, ctx):                      # when working with a cog, `self` goes before anything else in your command
    #    bot_latency = round(self.client.latency * 1000)
#
    #    await ctx.send(f"Pong! {bot_latency} ms.")
    
    
    @commands.hybrid_command(name="baller", description="yet another 8ball", with_app_command=True)
    @app_commands.describe(message="The question to ask")
    async def baller(self, ctx: commands.Context, *, message: str):
        async with aiofiles.open('responses.txt', mode='r') as f:
            random_responses = await f.readlines()
            response = random.choice(random_responses)
        
            #async for line in f:
            #    print(line)
        await ctx.defer()
        await asyncio.sleep(5)
        await ctx.send_message(response)
    
    
    @commands.command()          # commands use this decorator
    async def eightball(self, ctx, *, question):                      # when working with a cog, `self` goes before anything else in your command
        with open("responses.txt", "r") as f:        # "r" = read mode   
            random_responses = f.readlines()                    # file is being treated as a list
            response = random.choice(random_responses)
    
        await ctx.send(response)
    
    
    @commands.command(name="newballer", description="yet another 8ball")
    @app_commands.describe(message="The question to ask")
    async def newballer(self, ctx, *, message: str):
        async with aiofiles.open('responses.txt', mode='r') as f:
            random_responses = await f.readlines()
            response = random.choice(random_responses)
        
            #async for line in f:
            #    print(line)
        await ctx.defer()
        await asyncio.sleep(5)
        await ctx.send_message(response)
    
    
        
async def setup(client):
    await client.add_cog(Eightball(client))      #add_cog(NAME_OF_CLASS(client))   #case sensitive