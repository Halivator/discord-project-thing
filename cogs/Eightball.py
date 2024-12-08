import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import random
import aiofiles
import logging, logging.handlers
import os           #Q# os library is only used to get the TOKEN from the .env file


import sys
sys.path.append("..")

from base import Auth


logger = logging.getLogger(__name__)

class Eightball(commands.Cog):
    """
    Lets go gambling!
    AW DANG IT!\t\tAW DANG IT!
    AW DANG IT!\t\tAW DANG IT!
    """
    
    def __init__(self, client):
        self.client = client
    
    
    def custom_check():
        async def predicate(ctx):
            chk = False
            print(f'author id:\t{ctx.message.author.id}')
            print(f'dev id:\t\t{Auth.DEV_ID}')
            author = int(ctx.message.author.id)
            dev = int(Auth.DEV_ID)
            if author == dev:
                chk = True
                print(f'{chk}')
            return chk
        return commands.check(predicate)
    
    def second_check():
        async def predicate(ctx):
            chk = False
            print(f'author id:\t{ctx.message.author.id}')
            print(f'dev id:\t\t{Auth.DEV_ID}')
            author = int(ctx.message.author.id)
            dev = int(Auth.DEV_ID)
            if author != dev:
                chk = True
            print(f'{chk}')
            return chk
        return commands.check(predicate)

    
    @commands.Cog.listener()    # events use this decorator
    async def on_ready(self):
        print("Eightball.py is ready!")
    
    #@commands.command()          # commands use this decorator
    #async def eightball(self, ctx):                      # when working with a cog, `self` goes before anything else in your command
    #    bot_latency = round(self.client.latency * 1000)
#
    #    await ctx.send(f"Pong! {bot_latency} ms.")
    
    
    #@commands.hybrid_command(name="baller", description="yet another 8ball", with_app_command=True)
    #@app_commands.describe(message="The question to ask")
    #async def baller(self, ctx: commands.Context, *, message: str):
    #    async with aiofiles.open('eightball_responses.txt', mode='r') as f:
    #        random_responses = await f.readlines()
    #        response = random.choice(random_responses)
    #    
    #        #async for line in f:
    #        #    print(line)
    #    await ctx.defer()
    #    await asyncio.sleep(5)
    #    await ctx.send_message(response)
    #
    #
    #@commands.command()          # commands use this decorator
    #async def eightball(self, ctx, *, question):                      # when working with a cog, `self` goes before anything else in your #command
    #    with open("eightball_responses.txt", "r") as f:        # "r" = read mode   
    #        random_responses = f.readlines()                    # file is being treated as a list
    #        response = random.choice(random_responses)
    #
    #    await ctx.send(response)
    
    
    async def read_file_to_list(self, filename):
        """Reads lines from a file into a list of strings"""
        logger.info('Reading a file to list...')
        lines = []
        async with aiofiles.open(filename, mode='r') as f:
            async for line in f:
                lines.append(line.strip())
        return lines
    
    
    @commands.check_any(custom_check(), second_check())
    @commands.hybrid_command(name="tester", with_app_command=True, hidden=True)
    async def tester(self, ctx: commands.Context):
        
        await ctx.defer()
        await asyncio.sleep(5)
        await ctx.reply(f'yep ur a dev', mention_author=True)

    
    
    @commands.command(name="eightball", alias=["8b","magic_eightball","eight_ball"], description="yet another 8ball")
    @app_commands.describe(message="The question to ask")
    async def newballer(self, ctx, *, message: str = None):
        """Hey, Nerd! Here, have this Magic Eightball!
        
        (Ask the magic eightball a question and see what it has to say!)
        (For the developer: check out `eightball_responses.txt` to edit the responses)
        
        Args:
            message (str, optional): The question to ask. Defaults to None.
        """
        lines = []
        lines = await self.read_file_to_list('eightball_responses.txt')
        response = random.choice(lines)
        if message is not None:
            response = f"The answer to \"{message}\" is this: {response}"
            
        await ctx.defer()
        await asyncio.sleep(5)
        await ctx.send(f'{response}')
    
    
    
    #TODO: Fix the fact that Brax only seems to detect himself instead of the members within a channel
    @commands.hybrid_command(name="baller", alias=["ball", "b", "blr", "magic"], description="yet another 8ball", with_app_command=True)
    @app_commands.describe(message="What do you want now, Nerd?")
    async def baller(self, ctx: commands.Context, *, message: str):
        """Ha! Look how much cooler my eightball is compared to yours! I'll let you try it if you admit mine is cooler, Nerd!

        Args:
            message (str): _description_
        """
        members = ctx.channel.members #finds members connected to the channel

        memids = [] #(list)
        for member in members:
            print(f'{member}')
            memids.append(member)
            
        if message is not None:
            await ctx.send(f"\"{message}\", huh?", delete_after=25, silent=True)

        await ctx.send(f"Hmm...Let's see...", delete_after=25, silent=True)
        async with aiofiles.open('eightball_cooler_responses.txt', mode='r') as f:
            lines = []
            lines = await self.read_file_to_list('eightball_cooler_responses.txt')
            response = random.choice(lines)
            
            if '[USER]' in response:
                reslist = response.rsplit("[USER]")
                spy = random.choice(memids)
                response = (f'{reslist[0]}{member.mention}{reslist[1]}')
            
        await ctx.defer()
        await asyncio.sleep(5)
        await ctx.reply(f'{response}', mention_author=True)
    
    
        
async def setup(client):
    await client.add_cog(Eightball(client))      #add_cog(NAME_OF_CLASS(client))   #case sensitive