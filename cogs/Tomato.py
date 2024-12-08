### BraxCord Discord Bot
# Garden.py
# Created: 12/4/24 ~ 4:49pm
# Last Updated: 12/4/24 
# Code Source: ChatGPT: https://chatgpt.com/share/674ce36d-ba44-8002-a0f0-4cc8ceb814de
#############################################################################

from data_models import Wallet, Base
from data_models import UserGuild, Responses, Wallet, Base, async_session, initialize_db
from database_operations import add_to_userguild, get_from_userguild, delete_from_userguild, create_user_wallet, get_user_wallet, update_user_wallet, delete_user_wallet


import discord
from discord.ext import commands
from discord.ui import Button, View
import logging, logging.handlers
import asyncio

from sqlalchemy import create_engine, MetaData, Table 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os           #Q# os library is only used to get the TOKEN from the .env file


import random

import sys
sys.path.append("..")
from base import Auth

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./Bot.db" #data.db
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(bind=engine)

logger = logging.getLogger(__name__)

display_exception = True

gif_list=[]

# tomato throw
gif_list.append("https://tenor.com/nK758N5ESGK.gif")
# throwing tomatoes spongebob
gif_list.append("https://tenor.com/bZfRo.gif")

gif_fail = "https://tenor.com/view/sad-tomato-gif-14607666"

class TomatoToss(commands.Cog):
    """Let the tomatoes fly!!! Toss tomatoes at people and watch them lose money!"""
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="throw", description="Throw a tomato at someone and cause them to drop money.")
    async def throw(self, ctx: commands.Context, target: discord.Member):
        
        try:
            with Session() as session:
                user_id = str(ctx.author.id)
                random_drop = random.randint(1, 15)
                drop_amount = random_drop # This gets used in the output. It gets changed to a remainder later if the random_drop > balance

                #wallet = session.query(Wallet).filter_by(user_id=user_id).first()
                returned_wallet = await get_user_wallet(user_id)
                print(f'[{__name__}]:\t[returned_wallet]:\t<balance>: {returned_wallet.balance}\t<number_of_tomatoes>: {returned_wallet.number_of_tomatoes}\n\t<returned_wallet object>{returned_wallet}')
                balance = -1
                tomatoes = -1
                if returned_wallet: #If the wallet exists, display contents and balance
                    balance = returned_wallet.balance 
                    tomatoes = returned_wallet.number_of_tomatoes
                    print(f'[{__name__}]:\t[returned_wallet]:\tyour wallet balance is ${balance}\n\t You currently have {tomatoes} tomatoes')

                    temp_wallet = returned_wallet # made to temporarily store a wallet object. will get overwritten later
                    wallet_is_valid = False
                    will_drop_money = False

                    target_has_wallet = False
                    target_balance = -1
                    try:
                        target_wallet = await get_user_wallet(target.id)
                        if target_wallet: #If the wallet exists, display contents and balance
                            target_balance = target_wallet.balance
                            print(f'[{__name__}]:\t[target_wallet]:\tyour target\'s wallet balance is ${target_balance}')
                            print(f'[{__name__}]: [target_wallet]: [target_has_wallet]: True')
                            print(f'[{__name__}]:\t[target_wallet]:\t<balance>: {target_wallet.balance}\t<number_of_tomatoes>: {target_wallet.number_of_tomatoes}\n\t<returned_wallet object>{target_wallet}')
                            target_has_wallet = True
                            temp_wallet = target_wallet
                    except Exception as e:
                            print(f'EXCEPTION ENCOUNTERED: {e}')
                            print(f'[{__name__}]: [target_wallet]: [target_has_wallet]: False')

                    if returned_wallet:
                        print(f'[{__name__}]: [returned_wallet]: True')

                    if tomatoes > 0:
                        # Decrease the amount of tomatoes
                        tomatoes -= 1
                        returned_wallet.number_of_tomatoes = tomatoes
                        await update_user_wallet(user_id, returned_wallet)
                        result_wallet = await get_user_wallet(user_id)
                        # Compare wallets
                        if (returned_wallet.balance == result_wallet.balance and returned_wallet.number_of_tomatoes == result_wallet.number_of_tomatoes):
                            print(f'[{__name__}]:\t[returned_wallet]:\tThese have the same value')
                        
                        print(f'-----------------------------------------------------------------')
                        print(f'[{__name__}]:\t[   temp_wallet   ]:\t[user_id ]:\t{temp_wallet.user_id}')
                        print(f'[{__name__}]:\t[   temp_wallet   ]:\t[balance ]:\t{temp_wallet.balance}')
                        print(f'[{__name__}]:\t[   temp_wallet   ]:\t[tomatoes]:\t{temp_wallet.number_of_tomatoes}')
                        print(f'-----------------------------------------------------------------')
                        print(f'[{__name__}]:\t[ returned_wallet ]:\t[user_id ]:\t{returned_wallet.user_id}')
                        print(f'[{__name__}]:\t[ returned_wallet ]:\t[balance ]:\t{returned_wallet.balance}')
                        print(f'[{__name__}]:\t[ returned_wallet ]:\t[tomatoes]:\t{returned_wallet.number_of_tomatoes}')
                        print(f'-----------------------------------------------------------------')

                        if (temp_wallet.user_id != returned_wallet.user_id):
                            wallet_is_valid = True
                            print(f'[{__name__}]:\t[wallet_is_valid]:\tTrue')
                            
                            if (temp_wallet.balance > 0):
                                will_drop_money = True
                                print(f'[{__name__}]:\t[throw]\t{target.name} has money!')
                                if (temp_wallet.balance >= random_drop):
                                    # subtract the random_drop from the target's balance
                                    temp_wallet.balance -= random_drop
                                    result_wallet.balance += drop_amount
                                    await update_user_wallet(user_id,result_wallet)
                                    
                                elif (temp_wallet.balance < random_drop):
                                    #store the amount of balance your target had and set it to 0 
                                    drop_amount = temp_wallet.balance
                                    temp_wallet.balance = 0
                                    result_wallet.balance += drop_amount
                                    await update_user_wallet(user_id,result_wallet)
                            else:
                                print(f'[{__name__}]:\t[throw]\t{target.name} had no money to drop!')
                        
                        if will_drop_money and wallet_is_valid:
                            await update_user_wallet(target.id, temp_wallet)
                            print('temp wallet updated in the database')
                            

                            
                        gif_out = random.choice(gif_list)

                        await ctx.send(f'{ctx.author.mention} threw a tomato at {target.mention}', mention_author=True)
                        await asyncio.sleep(1)
                        await ctx.send(f'{gif_out}', mention_author=True)
                        await asyncio.sleep(1)
                        await ctx.send(f'`🍅x {result_wallet.number_of_tomatoes}` left!')
                        
                        await asyncio.sleep(1)
                        if wallet_is_valid is not True:
                            await ctx.send(f'{target.display_name} doesn\'t have a wallet!',silent=True, mention_author=False)
                        else:
                            if will_drop_money is True:
                                insult_to_injury = ""
                                if temp_wallet.balance <= 0: insult_to_injury = f" {target.display_name} has no more money!!"
                                await ctx.send(f'`{target.display_name} dropped ${drop_amount}.{insult_to_injury}`',silent=True, ephemeral=True, mention_author=False)
                            else:
                                await ctx.send(f'`{target.display_name} has no money to drop!`',silent=True, ephemeral=True, mention_author=False)

                    else:
                        #OUT OF TOMATOS
                        print(f'[{__name__}]: [returned_wallet]: False')
                        await ctx.followup.send(
                            "You're out of tomato's, bozo!!!",
                            ephemeral=True
                        )

                    
                    

        except Exception as e:
            printme = ""
            logger.error(f"[{__name__}]:\n\tError processing interaction:\n\t{e}\n----[END ERROR]----")
            if display_exception: printme = (f'\n`{__name__}`: `display_exception` `==` {display_exception}\n---\nException:\n>  {e}')
            await ctx.followup.send(f"Hmm... That didn't work? (try `!wallet`).{printme}", ephemeral=True)

        
        
        


    #@commands.hybrid_command(name="garden", description="Perform actions in your garden.")
    #async def garden(self, ctx: commands.Context, target: discord.Member):
    #    # Create an embed
    #    embed = discord.Embed(
    #        title="Garden Actions",
    #        description="Choose what you want to do in your Garden:",
    #        color=discord.Color.blue()
    #    )
    #    embed.add_field(name="Plant", value="Plant items in your garden.", inline=False)
    #    embed.add_field(name="Water", value="Water your garden.", inline=False)
    #    embed.set_footer(text="Use the buttons below to proceed.")
#
    #    # Create two buttons
    #    button1 = Button(label="Plant", style=discord.ButtonStyle.green)
    #    button2 = Button(label="Water", style=discord.ButtonStyle.blurple)
#
    #    # Create random values
    #    #random_plant = random.randint(1, 5)
    #    #random_water = random.randint(1, 3)
#
    #    # Define what happens when the "Plant" button is clicked
    #    async def button1_callback(interaction: discord.Interaction):
    #        await interaction.response.defer(ephemeral=True)
    #        random_plant = random.randint(1, 5)
#
    #        try:
    #            with Session() as session:
    #                user_id = str(interaction.user.id)
    #                #wallet = session.query(Wallet).filter_by(user_id=user_id).first()
    #                returned_wallet = await get_user_wallet(user_id)
    #                print(f'[{__name__}]:\t[returned_wallet]:\t<balance>: {returned_wallet.balance}\t<number_of_tomatoes>: {returned_wallet.number_of_tomatoes}\n\t<returned_wallet object>{returned_wallet}')
    #                balance = -1
    #                tomatoes = -1
    #                if returned_wallet: #If the wallet exists, display contents and balance
    #                    balance = returned_wallet.balance 
    #                    tomatoes = returned_wallet.number_of_tomatoes
    #                    print(f'[{__name__}]:\t[returned_wallet]:\tyour wallet balance is ${balance}\n\t You currently have {tomatoes} tomatoes')
#
#
#
    #                if returned_wallet:
    #                    print(f'[{__name__}]: [returned_wallet]: True')
    #                    tomatoes += random_plant
    #                    returned_wallet.number_of_tomatoes = tomatoes
    #                    
    #                    #session.commit()
    #                    
    #                    await update_user_wallet(user_id, returned_wallet)
    #                    result_wallet = await get_user_wallet(user_id)
#
    #                    if (returned_wallet.balance == result_wallet.balance and returned_wallet.number_of_tomatoes == result_wallet.number_of_tomatoes):
    #                        print(f'[{__name__}]:\t[returned_wallet]:\tThese have the same value')
#
    #                    logger.info(f"{interaction.user.display_name} planted {random_plant} tomatoes.")
    #                    await interaction.followup.send(
    #                        f"You planted {random_plant} tomatoes! Total tomatoes: {result_wallet.number_of_tomatoes}.",
    #                        ephemeral=True
    #                    )
    #                else:
    #                    print(f'[{__name__}]: [returned_wallet]: False')
    #                    await interaction.followup.send(
    #                        "You don't have a wallet yet! Use `!wallet` to register one!",
    #                        ephemeral=True
    #                    )
    #        except Exception as e:
    #            printme = ""
    #            logger.error(f"[{__name__}]:\n\tError processing interaction:\n\t{e}\n----[END ERROR]----")
    #            if display_exception: printme = (f'\n`GardenCog.py`: `display_exception` `==` {display_exception}\n---\nException:\n>  {e}')
    #            await interaction.followup.send(f"Hmm... That didn't work, have you already created your wallet? (try `!wallet`).{printme}", ephemeral=True)
#
    #    # Define what happens when the "Water" button is clicked
    #    async def button2_callback(interaction: discord.Interaction):
    #        await interaction.response.defer(ephemeral=True)
    #        random_water = random.randint(1, 3)
    #        try:
    #            with Session() as session:
    #                user_id = str(interaction.user.id)
    #                #wallet = session.query(Wallet).filter_by(user_id=user_id).first()
    #                returned_wallet = await get_user_wallet(user_id)
#
    #                print(f'[{__name__}]:\t[returned_wallet]:\t<balance>: {returned_wallet.balance}\t<number_of_tomatoes>: {returned_wallet.number_of_tomatoes}\n\t<returned_wallet object>{returned_wallet}')
    #                balance = -1
    #                tomatoes = -1
    #                if returned_wallet: #If the wallet exists, display contents and balance
    #                    balance = returned_wallet.balance 
    #                    tomatoes = returned_wallet.number_of_tomatoes
    #                    print(f'[{__name__}]:\t[returned_wallet]:\tyour wallet balance is ${balance}\n\t You currently have {tomatoes} tomatoes')
#
    #                if returned_wallet:
    #                    print(f'[{__name__}]: [returned_wallet]: True')
    #                    returned_wallet.number_of_tomatoes += random_water
    #                    tomatoes += random_water
    #                    returned_wallet.number_of_tomatoes = tomatoes
    #                    await update_user_wallet(user_id, returned_wallet)
    #                    result_wallet = await get_user_wallet(user_id)
#
    #                    if (returned_wallet.balance == result_wallet.balance and returned_wallet.number_of_tomatoes == result_wallet.number_of_tomatoes):
    #                        print(f'[{__name__}]:\t[returned_wallet]:\tThese have the same value')
#
    #                    logger.info(f"{interaction.user.display_name} watered their tomatoes and received {random_water} tomato(es).")
    #                    await interaction.followup.send(
    #                        f"You planted {random_water} tomatoes! Total tomatoes: {result_wallet.number_of_tomatoes}.",
    #                        ephemeral=True
    #                    )
    #                else:
    #                    print(f'[{__name__}]: [returned_wallet]: False')
    #                    await interaction.followup.send(
    #                        f"{interaction.user.display_name}, you don't have a wallet yet! Use `!wallet` to register one!",
    #                        ephemeral=True
    #                    )
    #        except Exception as e:
    #            printme = ""
    #            logger.error(f"[{__name__}]:\n\tError processing interaction:\n\t{e}\n----[END ERROR]----")
    #            if display_exception: printme = (f'\n`GardenCog.py`: `display_exception` `==` {display_exception}\n---\nException:\n>  {e}')
    #            await interaction.followup.send(f"Hmm... That didn't work, have you already created your wallet? (try `!wallet`).{printme}", ephemeral=True)
#
    #    # Assign the callbacks to the buttons
    #    button1.callback = button1_callback
    #    button2.callback = button2_callback
#
    #    # Create a View to hold the buttons
    #    view = View()
    #    view.add_item(button1)
    #    view.add_item(button2)
#
    #    # Send Information to the logger and terminal
    #    logger.info(f"[{__name__}]:\tGARDEN CALLED\n\t\tcontext: {ctx}")
    #    print(f"[{__name__}]:\tGARDEN CALLED\n\t\tcontext: {ctx}")
#
    #    # Send the message with the embed and buttons
    #    await ctx.send(embed=embed, view=view)

# Setup function for the cog
async def setup(bot):
    await bot.add_cog(TomatoToss(bot))     #add_cog(NAME_OF_CLASS(client))   #case sensitive