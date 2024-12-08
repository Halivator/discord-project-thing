### BraxCord Discord Bot
#FarmersMarket.py
# Created: 12/7/24 ~ 6:00pm
# Last Updated: 12/7/24 
# Code Source: ChatGPT: https://chatgpt.com/share/674ce36d-ba44-8002-a0f0-4cc8ceb814de
#############################################################################

from data_models import Wallet, Base
from data_models import UserGuild, Wallet, Base, async_session, initialize_db
from database_operations import add_to_userguild, get_from_userguild, delete_from_userguild, create_user_wallet, get_user_wallet, update_user_wallet, delete_user_wallet


import discord
from discord.ext import commands
from discord.ui import Button, View
import logging

from sqlalchemy import create_engine, MetaData, Table 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import random

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./Bot.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(bind=engine)

logger = logging.getLogger(__name__)

display_exception = True


class FarmersMarketCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="market", description="Perform actions in your garden.")
    async def market(self, ctx: commands.Context):
        """Buy or sell tomatoes at the Farmers Market! Be mindful of the current market value, though!"""
        balance = int(-1)
        
        # Create an embed
        embed = discord.Embed(
            title="Farmers Market Actions",
            description="Choose what you want to at the Farmers Market:",
            color=discord.Color.blue()
        )
        # Create random value
        random_price = random.randint(100, 500)
        
        embed.add_field(name=f"Current Market Value: ${random_price}", value="The cost of tomatoes change rapidly in this economy...", inline=False)
        embed.add_field(name=f" ",value="--------", inline=False)

        embed.add_field(name="Buy", value="Purchase a single tomato.", inline=False)
        embed.add_field(name="Sell", value="Sell a single tomato.", inline=False)
        embed.set_footer(text="Use the buttons below to proceed.")

        # Create two buttons
        button1 = Button(label="Buy", style=discord.ButtonStyle.green)
        button2 = Button(label="Sell", style=discord.ButtonStyle.red)


        # Define what happens when the "Buy" button is clicked
        async def button1_callback(interaction: discord.Interaction):
            await interaction.response.defer(ephemeral=True)

            try:
                with Session() as session:
                    user_id = str(interaction.user.id)
                    #wallet = session.query(Wallet).filter_by(user_id=user_id).first()
                    returned_wallet = await get_user_wallet(user_id)
                    print(f'[{__name__}]:\t[returned_wallet]:\t<balance>: {returned_wallet.balance}\t<number_of_tomatoes>: {returned_wallet.number_of_tomatoes}\n\t<returned_wallet object>{returned_wallet}')
                    #balance = -1
                    #tomatoes = -1
                    if returned_wallet: #If the wallet exists, display contents and balance
                        balance = returned_wallet.balance 
                        tomatoes = returned_wallet.number_of_tomatoes
                        print(f'[{__name__}]:\t[returned_wallet]:\tyour wallet balance is ${balance}\n\t You currently have {tomatoes} tomatoes')



                    if returned_wallet and returned_wallet.balance >= random_price:
                        print(f'[{__name__}]: [returned_wallet]: True')
                        tomatoes += 1
                        balance = returned_wallet.balance - random_price
                        returned_wallet.number_of_tomatoes = tomatoes
                        returned_wallet.balance = balance
                        
                        #session.commit()
                        
                        await update_user_wallet(user_id, returned_wallet)
                        result_wallet = await get_user_wallet(user_id)

                        if (returned_wallet.balance == result_wallet.balance and returned_wallet.number_of_tomatoes == result_wallet.number_of_tomatoes):
                            print(f'[{__name__}]:\t[returned_wallet]:\tThese have the same value')

                        logger.info(f"{interaction.user.display_name} bought 1 tomatoes for {random_price}.")
                        await interaction.followup.send(
                            f"You bought `1x 🍅` tomato for {random_price}! Total tomatoes: {result_wallet.number_of_tomatoes}.",
                            ephemeral=True
                        )
                    else:
                        print(f'[{__name__}]: [returned_wallet]: False')
                        await interaction.followup.send(
                            "You don't have enough money, twerp!",
                            ephemeral=True
                        )
            except Exception as e:
                printme = ""
                logger.error(f"[{__name__}]:\n\tError processing interaction:\n\t{e}\n----[END ERROR]----")
                if display_exception: printme = (f'\n`FarmersMarket.py`: `display_exception` `==` {display_exception}\n---\nException:\n>  {e}')
                await interaction.followup.send(f"Hmm... That didn't work, have you already created your wallet? (try `!wallet`).{printme}", ephemeral=True)

        # Define what happens when the "sell" button is clicked
        async def button2_callback(interaction: discord.Interaction):
            await interaction.response.defer(ephemeral=True)

            try:
                with Session() as session:
                    user_id = str(interaction.user.id)
                    returned_wallet = await get_user_wallet(user_id)

                    print(f'[{__name__}]:\t[returned_wallet]:\t<balance>: {returned_wallet.balance}\t<number_of_tomatoes>: {returned_wallet.number_of_tomatoes}\n\t<returned_wallet object>{returned_wallet}')
                    #balance = -1
                    #tomatoes = -1
                    if returned_wallet: #If the wallet exists, display contents and balance
                        balance = returned_wallet.balance 
                        tomatoes = returned_wallet.number_of_tomatoes
                        print(f'[{__name__}]:\t[returned_wallet]:\tyour wallet balance is ${balance}\n\t You currently have {tomatoes} tomatoes')

                    if returned_wallet and returned_wallet.number_of_tomatoes >= 1:
                        print(f'[{__name__}]: [returned_wallet]: True')
                        #returned_wallet.number_of_tomatoes += random_water
                        tomatoes -= 1
                        returned_wallet.number_of_tomatoes = tomatoes
                        balance += random_price
                        returned_wallet.balance = balance
                        await update_user_wallet(user_id, returned_wallet)
                        result_wallet = await get_user_wallet(user_id)

                        if (returned_wallet.balance == result_wallet.balance and returned_wallet.number_of_tomatoes == result_wallet.number_of_tomatoes):
                            print(f'[{__name__}]:\t[returned_wallet]:\tThese have the same value')

                        logger.info(f"{interaction.user.display_name} sold a tomato and received ${random_price}.")
                        await interaction.followup.send(
                            f"You sold a tomato for ${random_price}! Wallet Total: ${result_wallet.balance}. `🍅x {result_wallet.number_of_tomatoes}`",
                            ephemeral=True
                        )
                    else:
                        print(f'[{__name__}]: [returned_wallet]: False')
                        await interaction.followup.send(
                            f"You don't have any tomatoes`🍅` to sell, twerp!",
                            ephemeral=True
                        )
            except Exception as e:
                printme = ""
                logger.error(f"[{__name__}]:\n\tError processing interaction:\n\t{e}\n----[END ERROR]----")
                if display_exception: printme = (f'\n`FarmersMarket.py`: `display_exception` `==` {display_exception}\n---\nException:\n>  {e}')
                await interaction.followup.send(f"Hmm... That didn't work, have you already created your wallet? (try `!wallet`).{printme}", ephemeral=True)

        # Assign the callbacks to the buttons
        button1.callback = button1_callback
        button2.callback = button2_callback

        # Create a View to hold the buttons
        view = View()
        view.add_item(button1)
        view.add_item(button2)

        # Send Information to the logger and terminal
        logger.info(f"[{__name__}]:\tFARMERSMARKET CALLED\n\t\tcontext: {ctx}")
        print(f"[{__name__}]:\tFARMERSMARKET CALLED\n\t\tcontext: {ctx}")

        # Send the message with the embed and buttons
        await ctx.send(embed=embed, view=view)
        
        try:
            with Session() as session:
                user_id = str(ctx.author.id)
                returned_wallet = await get_user_wallet(user_id)
                balance = returned_wallet.balance
                tomato = returned_wallet.number_of_tomatoes
                await ctx.send(f"`💲{balance}\t🍅x{tomato}`", ephemeral=True)
        except Exception as e:
            printme = ""
            logger.error(f"[{__name__}]:\n\tError processing interaction:\n\t{e}\n----[END ERROR]----")
            if display_exception: printme = (f'\n`FarmersMarket.py`: `display_exception` `==` {display_exception}\n---\nException:\n>  {e}')
            await ctx.send(f"Hmm... That didn't work, have you already created your wallet? (try `!wallet`).{printme}", ephemeral=True)

        
# Setup function for the cog
async def setup(bot):
    await bot.add_cog(FarmersMarketCog(bot))     #add_cog(NAME_OF_CLASS(client))   #case sensitive
