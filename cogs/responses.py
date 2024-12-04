#from base import EconomyBot

import discord

from discord.ext import commands
from discord import app_commands
import logging, logging.handlers
import random
import asyncio
logger = logging.getLogger(__name__)


class Responses(commands.Cog):
    def __init__(self, bot): #client: EconomyBot):
        self.client = bot
        self.bank = self.client.db.bank
        self.inv = self.client.db.inv
        
        self.resp = self.client.db.resp
        
#    @commands.command(aliases=["inv"], usage="<member: @member>")
#    @commands.guild_only()
#    async def inventory(self, ctx, member: discord.Member = None):
#        user = member or ctx.author
#        user_av = user.display_avatar or user.default_avatar
#        if user.bot:
#            return await ctx.reply("Bot's don't have account", mention_author=False)
#        await self.inv.open_acc(user)
#
#        em = discord.Embed(color=0x00ff00)
#        x = 1
#        for item in self.inv.shop_items:
#            name = item["name"]
#            item_id = item["id"]
#
#            data = await self.inv.update_acc(user, 0, name)
#            if data[0] >= 1:
#                x += 1
#                em.add_field(
#                    name=f"{name.upper()} - {data[0]}", value=f"ID: {item_id}", inline=False)
#
#        em.set_author(name=f"{user.name}'s Inventory", icon_url=user_av.url)
#        if x == 1:
#            em.description = "The items which you bought display here..."
#
#        await ctx.reply(embed=em, mention_author=False)
#



    @commands.Cog.listener("on_message")    # events use this decorator
    @commands.guild_only()
    async def responder(self, message):
        print(f'{message.author.id} | {message.channel.name} | {message.content}')
        
        command_container = []
        # iterating through cogs
        # getting commands from cog
        for cog in self.client.cogs:
            for command in self.client.get_cog(cog).get_commands():
                command_container.append(command.name)
        # integrating through uncategorized commands
        for command in self.client.walk_commands():
            # if cog not in a cog
            if not command.cog_name: # and not command.hidden:
                command_container.append(command.name)
        
        
        if message.author == self.client.user:
            print(f'{__name__}:\t{message.author.name} is the same as self.user. Returning....')
            return
        #print(f'{__name__}:\t{message.author.name} is NOT the same as self.user. Continuing....') # for debugging

        for cmd in command_container:
            if (cmd in message.content):
                print(f'{__name__}:\tCOMMAND ATTEMPTED. ABORTING RESPONDER')
                return


        options = []
        await self.resp.open_resp(message.guild)
        data = await self.resp.get_resp(message.guild, message.content)
        #bdata = await self.resp.nget_resp(message.guild, message.content)
        #cdata = await self.resp.sget_resp(message.guild, message.content)
        checker = False
        if data is not None:
                checker = True
        print(f'{__name__}: [data]: has data?\t{checker}')
        
        #if message.guild.id not in [ resps["message_to_detect"] for resps in data]:

        #wordber = message.content.split(' ')
        #for word in wordber:
        #print(f'{word} is {type(word)} type')
        if message.content in [ resps[2] for resps in data]:
            print(f'{message.content} found in get_resp')
            options = await self.resp.sget_resp(message.guild, message.content)
            
            print(f'{__name__}: [options]: [PRINTING LOOP...]')
            for row in options:
                print(f"\t- responseID[0]: {row[0]}, guildID[1]: {row[1]}, message_to_detect[2]: {row[2]}, output[3]: {row[3]}")  # Replace with actual columns
            print(f'{__name__}: [options]: [END LOOP...]')
            opt = random.choice(options)
            print(f'{opt[3]}')
            await message.channel.send(f'{opt[3]}')
        #for resps in data:
        #    if word in resps[2]:
        #        print(f'{word} found')
        #    else:
        #        print(f'{word} not found')
        


                
        



        
        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')
        
        if message.content.startswith('$gambling'):
            #do gambling
            await message.channel.send("Aw dang it!")
        
    
        await self.client.process_commands(message)
        print(f'> {message.author.name} | {message.channel.name} | {message.content}')



    @commands.hybrid_command(usage="<item_name*: string>", with_app_command=True)
    @commands.guild_only()
    async def addnewdetect(self, ctx: commands.Context, detect_phrase: str, output_line: str):
        guild = ctx.guild
        await self.resp.open_resp(guild)
        #item_name.lower()
        #if detect_phrase not in [item["name"].lower() for item in self.inv.shop_items]:
        #    return await ctx.reply(f"Theirs no item named `{item_name}`", mention_author=False)

    #    resps = await self.resp.get_resp(guild)
#        for respo in resps:
#            if item_name == item["name"].lower():
#
#                if users[1] < item["cost"]:
#                    return await ctx.reply(f"You don't have enough money to buy {item['name']}",
#                                           mention_author=False)

        result = await self.resp.create_resp(guild, detect_phrase, output_line)
        #await self.bank.update_acc(user, -item["cost"])
        
        
        await ctx.defer()
        await asyncio.sleep(5)
        return await ctx.reply(f"Added a new response: detects[{result[2]}] | outputs[{result[3]}] | Number of Responses for this guild: {result[0]}", mention_author=False)

        
#
#    @commands.command(usage="<item_name*: string>")
#    async def addgif(self, ctx, *, item_name: str):
#        
#        
#        
#        return await ctx.reply(f"end of method")



#    @commands.command(usage="<item_name*: string>")
#    async def buy(self, ctx, *, item_name: str):
#        user = ctx.author
#        await self.bank.open_acc(user)
#        await self.inv.open_acc(user)
#        if item_name.lower() not in [item["name"].lower() for item in self.inv.shop_items]:
#            return await ctx.reply(f"Theirs no item named `{item_name}`", mention_author=False)
#
#        users = await self.bank.get_acc(user)
#        for item in self.inv.shop_items:
#            if item_name == item["name"].lower():
#
#                if users[1] < item["cost"]:
#                    return await ctx.reply(f"You don't have enough money to buy {item['name']}",
#                                           mention_author=False)
#
#                await self.inv.update_acc(user, +1, item["name"])
#                await self.bank.update_acc(user, -item["cost"])
#                return await ctx.reply(f"You bought {item_name}", mention_author=False)
#
#    @commands.command(usage="<item_name*: string>")
#    async def sell(self, ctx, *, item_name: str):
#        user = ctx.author
#        await self.bank.open_acc(user)
#        await self.inv.open_acc(user)
#        if item_name.lower() not in [item["name"].lower() for item in self.inv.shop_items]:
#            return await ctx.reply(f"Theirs no item named `{item_name}`", mention_author=False)
#
#        for item in self.inv.shop_items:
#            if item_name.lower() == item["name"].lower():
#                cost = int(round(item["cost"] / 2, 0))
#                quantity = await self.inv.update_acc(user, 0, item["name"])
#                if quantity[0] < 1:
#                    return await ctx.reply(f"You don't have {item['name']} in your inventory",
#                                           mention_author=False)
#
#                await self.inv.update_acc(user, -1, item["name"])
#                await self.bank.update_acc(user, +cost)
#                return await ctx.reply(f"You sold {item_name} for {cost:,}", mention_author=False)
#

# if you are using 'discord.py >=v2.0' comment(remove) below code
#def setup(client):
#    client.add_cog(Inventory(client))

# if you are using 'discord.py >=v2.0' uncomment(add) below code
async def setup(client):
     await client.add_cog(Responses(client))
