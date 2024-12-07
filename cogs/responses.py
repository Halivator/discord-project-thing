#from base import EconomyBot
"""
Q

Adapted from Economy Bot's inventory, mainbank, and shop cogs

Makes use of the module responses_funcs.py

"""


import discord

from discord.ext import commands
from discord import app_commands
import logging, logging.handlers
import random
import asyncio
logger = logging.getLogger(__name__)


class Responses(commands.Cog):
    """
    Controls Brax's phrases to respond to!
    
    Uses a separate database from the economy.

    Needs to be tweaked to account for case sensitivity and substring detection.
    
    Utilizes Debugging Verbosity levels that are detailed in `modules/responses_funcs.py`.
    - To set the desired verbosity levels for your terminal window, edit the parameters in `modules/__init__.py`
    
    Args:
        commands (_type_): _description_
    """
    def __init__(self, bot): #client: EconomyBot):
        self.client = bot
        #self.bank = self.client.db.bank
        #self.inv = self.client.db.inv
        
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
        
        
        #skip = False    # Determines if the subsequent steps should be skipped
        
        if message.author == self.client.user:
            if self.resp._v4check():
                print(f'>\t{message.author.name} | {message.channel.name} | {message.content}')
            if self.resp._v3check():
                print(f'{__name__}:\t{message.author.name} is the same as self.user. Returning....')
            return
        else:
            print(f'>\t{message.author.name} | {message.channel.name} | {message.content}')
        
        
        
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
        
        
        #print(f'{__name__}:\t{message.author.name} is NOT the same as self.user. Continuing....') # for debugging

        for cmd in command_container:
            if (cmd in message.content):
                if self.resp._v3check(): print(f'{__name__}:\tCOMMAND ATTEMPTED. ABORTING RESPONDER')
                return


        options = []
        await self.resp.open_resp(message.guild)
        data = await self.resp.get_resp(message.guild, message.content)
        #bdata = await self.resp.nget_resp(message.guild, message.content)
        #cdata = await self.resp.sget_resp(message.guild, message.content)
        checker = False
        if data is not None:
                checker = True
        if self.resp._v3check(): print(f'{__name__}: [data]: has data?\t{checker}')
        
        #if message.guild.id not in [ resps["message_to_detect"] for resps in data]:

        #wordber = message.content.split(' ')
        #for word in wordber:
        #print(f'{word} is {type(word)} type')
        
        
        original_value = None
        for resps in data:
            if self.resp._v3check(): print(f'looping!!')
            if message.content.lower() == resps[2].lower():
                original_value = resps[2]
                if self.resp._v3check(): print(f'original_value set!')
            else:
                if self.resp._v3check(): print('Nope!!')
        
        #TODO: figure out work around for case sensitivity... I worry it might have to be done by starting from scratch again, but for now i'm done \(>~<)/ --Q
        #print(f'{message.content.lower()}')
        #
        ## Using next with a generator to find the matching 'resps'
        #matching_resps = next(
        #    (resps for resps in data if message.content.lower() == [resps[2]].lower()), 
        #    None
        #)
#
        #if matching_resps:
        #    print(f"Original value of resps[2]: {matching_resps[2]}")
        #    print(f"lowered value of resps[2]: {matching_resps[2].lower()}")
        #else:
        #    print("No match found for the message content.")

        
        
        
        if message.content in [ resps[2] for resps in data]:
            
            if self.resp._v1check(): print(f'{__name__}\t{message.content} found in get_resp')
            
            
            options = await self.resp.sget_resp(message.guild, original_value) #message.content
            
            if self.resp._v2check():
                print(f'{__name__}: [options]: [PRINTING LOOP...]')
                for row in options:
                    print(f"\t- responseID[0]: {row[0]}, guildID[1]: {row[1]}, message_to_detect[2]: {row[2]}, output[3]: {row[3]}")  # Replace with actual columns
                print(f'{__name__}: [options]: [END LOOP...]')
            opt = random.choice(options)
            if self.resp._v1check(): print(f'{__name__}:\n[OUTPUT]:\t\t{opt[3]}')
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






    @commands.hybrid_command(with_app_command=True)
    @app_commands.describe(
    detect_phrase='What should Brax respond to? Case sensitive. NOTE: should contain the whole message that Brax responds to. Substrings are broken atm',
    output_line='The phrase or tenor gif link that Brax should respond using',
)
    @commands.guild_only()
    async def add_new_detect(self, ctx: commands.Context, detect_phrase: str, output_line: str):
        """Add a new Response for Brax to use!
        
        Choose a phrase for Brax to detect (case sensitive, and should include the whole message that Brax will respond to)
        
        *GOAL FOR LATER: adjust listener or `responses_funcs` to detect substrings of messages and to tweak case sensitivity*
        
        When specifying a gif link, try to specify a direct https:// link to the gif, ending in `.gif`. This is what allows Discord to display the gif as an embed.
        
        Args:
            detect_phrase (str): _description_
            output_line (str): _description_
        """
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
        
        

        #counter = await self.resp.count_resp(guild)
        
        await ctx.defer()
        await asyncio.sleep(5)
        return await ctx.reply(f"Added a new response: detects[{result[2]}] | outputs[{result[3]}] | Number of Responses for this guild: [BROKEN FEATURE]", mention_author=False, silent=True)












    @commands.hybrid_command(usage="<item_name*: string>", with_app_command=True)
    @commands.guild_only()
    async def edit_detect(self, ctx: commands.Context, detect_phrase: str, output_line: str, new_detect_phrase: str, new_output_line: str):
        """currently broken"""
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

        result = await self.resp.s_update_resp(guild, detect_phrase, output_line, new_detect_phrase, new_output_line)
        #await self.bank.update_acc(user, -item["cost"])
        
        
       # options = await self.resp.oget_resp(guild, new_detect_phrase, new_output_line)
            
            
       # print(f'{__name__}: [options]: [PRINTING LOOP...]')
        #for row in options:
        #    print(f"\t- responseID[0]: {row[0]}, guildID[1]: {row[1]}, message_to_detect[2]: {row[2]}, output[3]: {row[3]}")  # Replace with actual columns
        #print(f'{__name__}: [options]: [END LOOP...]')


        
        await ctx.defer()
        await asyncio.sleep(5)
        return await ctx.reply(f"Edited a response", mention_author=False)






    #delete_after, silent

    @commands.hybrid_command(with_app_command=True)
    @app_commands.describe(
    detect_phrase='What should Brax respond to? Case sensitive. NOTE: should contain the whole message that Brax responds to. Substrings are broken atm',
    output_line='The phrase or tenor gif link that Brax should respond using',
    )
    @commands.guild_only()
    async def delete_detect_resp(self, ctx: commands.Context, detect_phrase: str, output_line: str):
        """Delete a specific Response set from Brax's database for this server!
        
        **NOTE:** It is *highly* recommended to run `!list_resp` before using this command!

        """
        guild = ctx.guild
        data = await self.resp.open_resp(guild)
        res = ""
        
        await ctx.defer()

        
        if detect_phrase in [ resps[2] for resps in data]:
            #await ctx.defer()
            await ctx.send(f"Match found!")
            #result =
            await self.resp.delete_output_resp(guild, detect_phrase, output_line)
            # ensure that the row has been successfully deleted
            await asyncio.sleep(5)
            result_set = await self.resp.oget_resp(guild, detect_phrase, output_line)
            if result_set is None:
                res = "success!"
            elif result_set is not None:
                res = f'failure! {result_set[2]} was found with {result_set[3]}'
            #for row in data:
                #print(f"row is '{type(row)}'")
                #print(f"\t{c}:\t responseID[0]: {row[0]}, guildID[1]: {row[1]}, message_to_detect[2]: {row[2]}, output[3]: {row[3]}")  # DEBUG
                #await ctx.send(f"detects[\" {row[2]} \"]\t|\toutputs[\" {row[3]} \"]")

        elif detect_phrase not in [ resps[2] for resps in data]:
            await ctx.send(f"Match not found!")
            res = "not found!"

        
        
        
        #await ctx.defer()
        await asyncio.sleep(5)
        return await ctx.reply(f"Attempted to delete a response set:\ndetects[\' {detect_phrase} \'] | outputs[\' {output_line} \']\nRESULT: {res}", mention_author=False, silent=True)




    @commands.command(usage="<item_name*: string>", with_app_command=True)
    @commands.guild_only()
    async def list_resp(self, ctx): #commands.Context):
        """Lists all of Brax's Response sets registered for this server!
        
        Will cycle through the database, and finish by stating how many responses have been registered

        Listed responses will disappear from the chat after a set amount of time (3 minutes) to keep the chat clear.
        
        Args:
            self (_type_): _description_
        """
        del_in_min = 3
        delete_after_seconds = del_in_min * 60
        guild = ctx.guild
        data = await self.resp.open_resp(guild)
        
#        data = await self.resp.get_all_resp(guild)
        checker = False
        #count = 0
        await ctx.defer()
        if data is not None:
                checker = True
        #        count = self.resp.count_resp(guild)

        if self.resp._v3check(): print(f'{__name__}: [data]: has data?\t{checker}') # DEBUG

        messenger = ctx.message # used to get around ctx limitations

        if checker == True:

            #tester = self.ctr(data)
            #print (f"{tester}")
            #print(f"{__name__}: [list_resp]:\t{tester} responses returned\n") # DEBUG
            
            c = 0
            await ctx.send(f"Listing Responses. Please wait until I am finished...", delete_after=30)

            for row in data:
                if self.resp._v2check():
                    if self.resp._v3check(): print(f"row is '{type(row)}'")
                    if self.resp._v4check(): print(f"\t{c}:\t responseID[0]: {row[0]}, guildID[1]: {row[1]}, message_to_detect[2]: {row[2]}, output[3]: {row[3]}")  # DEBUG
                await ctx.send(f"detects[\" {row[2]} \"]\t|\toutputs[\" {row[3]} \"]", delete_after=delete_after_seconds)

                #await self.row_sender(messenger, row) # BROKEN + NOT NEEDED
                c = c + 1

#            await ctx.defer()
            await asyncio.sleep(5)
            await ctx.send(f"All done! List of Responses will disappear after {del_in_min} minutes!", delete_after=delete_after_seconds)
            return await ctx.reply(f"Responses found: {c}", mention_author=False)
        else:
#            await ctx.defer()
            return await ctx.reply(f"No responses found!", mention_author=False)
        
    #    if not ctx.channel.is_nsfw():
    #        embed = discord.Embed(
    #            title=":x: Channel Is Not NSFW",
    #            color=discord.Colour.purple()
    #        )
    #        embed.set_image(url="https://media0.giphy.com/media/W5C9c8nqoaDJWh34i6/giphy.gif")
    #        embed.set_image(url="https://giphy.com/gifs/W5C9c8nqoaDJWh34i6")
    #    else:
    #        async with ctx.channel.typing():
    #            memes_submissions = reddit.subreddit("rule34").hot()
    #            post_to_pick = random.randint(1, 10)
    #            for i in range(0, post_to_pick):
    #                submission = memes_submissions.__next__()
    #            embed = discord.Embed(
    #                title=submission.title,
    #                 color=discord.Colour.purple()
    #            )
    #            embed.set_image(url=submission.url)
    #            embed.add_field(name="Author", value="u/" + submission.author.name, )
    #            embed.add_field(name="View Online", value=f"[Link]({submission.url})", )
    #            embed.add_field(name="Subreddit", value="r/rule34", )
    #    await ctx.send(embed=embed)


    async def row_sender(self, messenger, row):
        """unused, I think? -Q"""
        return await messenger.channel.send(f"detects[\" {row[2]} \"]\t|\toutputs[\" {row[3]} \"]", mention_author=False)

    async def row_count_sender(self, messenger, row, currentCount):
        """unused, I think? -Q"""
        return await messenger.channel.send(f"{currentCount}:\ndetects[\" {row[2]} \"]\t|\toutputs[\" {row[3]} \"]", mention_author=False)

    async def row_looper(self, data):    
        """unused, I think? -Q"""
        for i in range(1, data + 1):
            print(i)
        await asyncio.sleep(1)
        
    async def pooper(self, toople):
        """unused, I think? -Q"""
        c = 1
        for row in toople:
            print(f"row is '{type(row)}'")
            print(f"\t{c}:\t responseID[0]: {row[0]}, guildID[1]: {row[1]}, message_to_detect[2]: {row[2]}, output[3]: {row[3]}")  # DEBUG
            c=c+1
        await asyncio.sleep(1)


    def ctr(self, look):
        """This one gets used but i cant remember if it works or not - Q"""
        c = 0
        for row in look:
            c=c+1
            print(f'{c}')
        return c
        
    async def gatherer(self):
        tasks = [
            asyncio.create_task(self.row_looper(10)),
            asyncio.create_task(self.row_looper(7)),
        ]
        await asyncio.gather(*tasks)
        
#
#    @commands.command(usage="<item_name*: string>")
#    async def addgif(self, ctx, *, item_name: str):
#        
#        
#        
#        return await ctx.reply(f"end of method")

#    @commands.command(hidden=True, with_app_command=True)
#    @commands.guild_only()
#    async def list_resp_absolutely_all(self, ctx): #commands.Context):
#        """Lists all of Brax's Response sets registered for this server!
#        
#        Will cycle through the database, and finish by stating how many responses have been registered
#
#        Listed responses will disappear from the chat after a set amount of time (3 minutes) to keep the chat clear.
#        
#        Args:
#            self (_type_): _description_
#        """
#        del_in_min = 3
#        delete_after_seconds = del_in_min * 60
#        guild = ctx.guild
#        data = await self.resp.open_resp(guild)
#        
##        data = await self.resp.get_all_resp(guild)
#        checker = False
#        count = 0
#        await ctx.defer()
#        if data is not None:
#                checker = True
#                count = self.resp.count_resp(guild)
#
#        print(f'{__name__}: [data]: has data?\t{checker}') # DEBUG
#
#        messenger = ctx.message # used to get around ctx limitations
#
#        if checker == True:
#            print(f"{__name__}: [list_resp]:\t{count} responses returned\n") # DEBUG
#
#            tester = self.ctr(data)
#            print (f"{tester}")
#            
#            c = 1
#            
#            for row in data:
#                print(f"row is '{type(row)}'")
#                print(f"\t{c}:\t responseID[0]: {row[0]}, guildID[1]: {row[1]}, message_to_detect[2]: {row[2]}, output[3]: {row[3]}")  # DEBUG
#                await ctx.send(f"detects[\" {row[2]} \"]\t|\toutputs[\" {row[3]} \"]", delete_after=delete_after_seconds)
#                
#                #await self.row_sender(messenger, row)
#                c = c + 1
#
##            await ctx.defer()
#            await asyncio.sleep(5)
#            return await ctx.reply(f"Responses found: {c}", mention_author=False)
#        else:
##            await ctx.defer()
#            return await ctx.reply(f"No responses found!", mention_author=False)







#    @commands.command(hidden=True)
#    async def get_userid(self, ctx, member: discord.Member):
#        """Gets the userid of the pinged user."""
#        logger.info('grabbing user id')
#        username = member.name
#        uid = member.id
#        
#        print(f'{ctx.user.display_name} ({ctx.user.name}): grabbed [{username}]\'s id: {uid}')
#        return await ctx.response.send_message(f'Check the terminal window...', ephemeral = True, delete_after=10)










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
