### BraxCord Discord Bot
# Garden.py
# Created: 12/4/24 ~ 4:49pm
# Last Updated: 12/4/24 
# Code Source: ChatGPT: https://chatgpt.com/share/674ce36d-ba44-8002-a0f0-4cc8ceb814de
#############################################################################
#TEst comment
import discord
from discord.ext import commands
from discord.ui import Button, View
import logging

from sqlalchemy import create_engine, MetaData, Table 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from data_models import Wallet, Base

import random

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./data.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(bind=engine)

logger = logging.getLogger(__name__)

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
        random_plant = random.randint(1, 5)
        random_water = random.randint(1, 3)

        # Define what happens when the "Plant" button is clicked
        async def button1_callback(interaction: discord.Interaction):
            await interaction.response.defer(ephemeral=True)
            try:
                with Session() as session:
                    user_id = str(interaction.user.id)
                    wallet = session.query(Wallet).filter_by(user_id=user_id).first()

                    if wallet:
                        wallet.number_of_tomatoes += random_plant
                        session.commit()
                        logger.info(f"{interaction.user.display_name} planted {random_plant} tomatoes.")
                        await interaction.followup.send(
                            f"You planted {random_plant} tomatoes! Total tomatoes: {wallet.number_of_tomatoes}.",
                            ephemeral=True
                        )
                    else:
                        await interaction.followup.send(
                            "You don't have a wallet yet!",
                            ephemeral=True
                        )
            except Exception as e:
                logger.error(f"Error processing interaction: {e}")
                await interaction.followup.send("An error occurred. Please try again later.", ephemeral=True)

        # Define what happens when the "Water" button is clicked
        async def button2_callback(interaction: discord.Interaction):
            await interaction.response.defer(ephemeral=True)
            try:
                with Session() as session:
                    user_id = str(interaction.user.id)
                    wallet = session.query(Wallet).filter_by(user_id=user_id).first()

                    if wallet:
                        wallet.number_of_tomatoes += random_water
                        session.commit()
                        logger.info(f"{interaction.user.display_name} watered their tomatoes and received {random_water} tomato(es).")
                        await interaction.followup.send(
                            f"{interaction.user.display_name} watered their tomatoes and received {random_water} tomato(es).",
                            ephemeral=True
                        )
                    else:
                        await interaction.followup.send(
                            "Error. {interaction.user.display_name} does not have a wallet.",
                            ephemeral=True
                        )
            except Exception as e:
                logger.error(f"Error processing interaction: {e}")
                await interaction.followup.send("An error occurred. Please try again later.", ephemeral=True)

        # Assign the callbacks to the buttons
        button1.callback = button1_callback
        button2.callback = button2_callback

        # Create a View to hold the buttons
        view = View()
        view.add_item(button1)
        view.add_item(button2)

        # Send Information to the logger and terminal
        logger.info(f"GARDEN CALLED\n\tcontext: {ctx}")
        print(f"GARDEN CALLED\n\tcontext: {ctx}")

        # Send the message with the embed and buttons
        await ctx.send(embed=embed, view=view)

# Setup function for the cog
async def setup(bot):
    await bot.add_cog(GardenCog(bot))     #add_cog(NAME_OF_CLASS(client))   #case sensitive