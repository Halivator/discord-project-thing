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
import logging

from sqlalchemy import create_engine, MetaData, Table 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import random

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./Bot.db" #data.db
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(bind=engine)

logger = logging.getLogger(__name__)

display_exception = True


class GardenCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="garden", description="Perform actions in your garden.")
    async def garden(self, ctx: commands.Context):
        # Create an embed
        embed = discord.Embed(
            title="Garden Actions",
            description="Choose what you want to do in your Garden:",
            color=discord.Color.blue()
        )
        embed.add_field(name="Plant", value="Plant items in your garden.", inline=False)
        embed.add_field(name="Water", value="Water your garden.", inline=False)
        embed.set_footer(text="Use the buttons below to proceed.")

        # Create two buttons
        button1 = Button(label="Plant", style=discord.ButtonStyle.green)
        button2 = Button(label="Water", style=discord.ButtonStyle.blurple)

        # Create random values
        #random_plant = random.randint(1, 5)
        #random_water = random.randint(1, 3)

        # Define what happens when the "Plant" button is clicked
        async def button1_callback(interaction: discord.Interaction):
            await interaction.response.defer(ephemeral=True)
            random_plant = random.randint(1, 5)

            try:
                with Session() as session:
                    user_id = str(interaction.user.id)
                    #wallet = session.query(Wallet).filter_by(user_id=user_id).first()
                    returned_wallet = await get_user_wallet(user_id)
                    print(f'[{__name__}]:\t[returned_wallet]:\t<balance>: {returned_wallet.balance}\t<number_of_tomatoes>: {returned_wallet.number_of_tomatoes}\n\t<returned_wallet object>{returned_wallet}')
                    balance = -1
                    tomatoes = -1
                    if returned_wallet: #If the wallet exists, display contents and balance
                        balance = returned_wallet.balance 
                        tomatoes = returned_wallet.number_of_tomatoes
                        print(f'[{__name__}]:\t[returned_wallet]:\tyour wallet balance is ${balance}\n\t You currently have {tomatoes} tomatoes')



                    if returned_wallet:
                        print(f'[{__name__}]: [returned_wallet]: True')
                        tomatoes += random_plant
                        returned_wallet.number_of_tomatoes = tomatoes
                        
                        #session.commit()
                        
                        await update_user_wallet(user_id, returned_wallet)
                        result_wallet = await get_user_wallet(user_id)

                        if (returned_wallet.balance == result_wallet.balance and returned_wallet.number_of_tomatoes == result_wallet.number_of_tomatoes):
                            print(f'[{__name__}]:\t[returned_wallet]:\tThese have the same value')

                        logger.info(f"{interaction.user.display_name} planted {random_plant} tomatoes.")
                        await interaction.followup.send(
                            f"You planted {random_plant} tomatoes! Total tomatoes: {result_wallet.number_of_tomatoes}.",
                            ephemeral=True
                        )
                    else:
                        print(f'[{__name__}]: [returned_wallet]: False')
                        await interaction.followup.send(
                            "You don't have a wallet yet! Use `!wallet` to register one!",
                            ephemeral=True
                        )
            except Exception as e:
                printme = ""
                logger.error(f"[{__name__}]:\n\tError processing interaction:\n\t{e}\n----[END ERROR]----")
                if display_exception: printme = (f'\n`GardenCog.py`: `display_exception` `==` {display_exception}\n---\nException:\n>  {e}')
                await interaction.followup.send(f"Hmm... That didn't work, have you already created your wallet? (try `!wallet`).{printme}", ephemeral=True)

        # Define what happens when the "Water" button is clicked
        async def button2_callback(interaction: discord.Interaction):
            await interaction.response.defer(ephemeral=True)
            random_water = random.randint(1, 3)
            try:
                with Session() as session:
                    user_id = str(interaction.user.id)
                    #wallet = session.query(Wallet).filter_by(user_id=user_id).first()
                    returned_wallet = await get_user_wallet(user_id)

                    print(f'[{__name__}]:\t[returned_wallet]:\t<balance>: {returned_wallet.balance}\t<number_of_tomatoes>: {returned_wallet.number_of_tomatoes}\n\t<returned_wallet object>{returned_wallet}')
                    balance = -1
                    tomatoes = -1
                    if returned_wallet: #If the wallet exists, display contents and balance
                        balance = returned_wallet.balance 
                        tomatoes = returned_wallet.number_of_tomatoes
                        print(f'[{__name__}]:\t[returned_wallet]:\tyour wallet balance is ${balance}\n\t You currently have {tomatoes} tomatoes')

                    if returned_wallet:
                        print(f'[{__name__}]: [returned_wallet]: True')
                        returned_wallet.number_of_tomatoes += random_water
                        tomatoes += random_water
                        returned_wallet.number_of_tomatoes = tomatoes
                        await update_user_wallet(user_id, returned_wallet)
                        result_wallet = await get_user_wallet(user_id)

                        if (returned_wallet.balance == result_wallet.balance and returned_wallet.number_of_tomatoes == result_wallet.number_of_tomatoes):
                            print(f'[{__name__}]:\t[returned_wallet]:\tThese have the same value')

                        logger.info(f"{interaction.user.display_name} watered their tomatoes and received {random_water} tomato(es).")
                        await interaction.followup.send(
                            f"You planted {random_water} tomatoes! Total tomatoes: {result_wallet.number_of_tomatoes}.",
                            ephemeral=True
                        )
                    else:
                        print(f'[{__name__}]: [returned_wallet]: False')
                        await interaction.followup.send(
                            f"{interaction.user.display_name}, you don't have a wallet yet! Use `!wallet` to register one!",
                            ephemeral=True
                        )
            except Exception as e:
                printme = ""
                logger.error(f"[{__name__}]:\n\tError processing interaction:\n\t{e}\n----[END ERROR]----")
                if display_exception: printme = (f'\n`GardenCog.py`: `display_exception` `==` {display_exception}\n---\nException:\n>  {e}')
                await interaction.followup.send(f"Hmm... That didn't work, have you already created your wallet? (try `!wallet`).{printme}", ephemeral=True)

        # Assign the callbacks to the buttons
        button1.callback = button1_callback
        button2.callback = button2_callback

        # Create a View to hold the buttons
        view = View()
        view.add_item(button1)
        view.add_item(button2)

        # Send Information to the logger and terminal
        logger.info(f"[{__name__}]:\tGARDEN CALLED\n\t\tcontext: {ctx}")
        print(f"[{__name__}]:\tGARDEN CALLED\n\t\tcontext: {ctx}")

        # Send the message with the embed and buttons
        await ctx.send(embed=embed, view=view)

# Setup function for the cog
async def setup(bot):
    await bot.add_cog(GardenCog(bot))     #add_cog(NAME_OF_CLASS(client))   #case sensitive