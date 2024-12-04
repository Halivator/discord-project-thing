### BraxCord Discord Bot
# Garden.py
# Created: 12/4/24 ~ 4:49pm
# Last Updated: 12/4/24 
# Code Source: 
#############################################################################

import discord
from discord.ext import commands
from discord.ui import Button, View

from discord     import app_commands
import asyncio
import logging
import logging.handlers

logger = logging.getLogger(__name__)

class GardenCog(commands.Cog):

    def __init__(self, bot):     #bot
        self.bot = bot          #self.bot = bot

    @commands.hybrid_command(name="garden", description="Create an embed test of the garden market")
    async def garden(self, ctx: commands.Context):
      # Create an embed
      embed = discord.Embed(
          title="Garden Actions",
          description="Choose what you want to do in your Garden:",
          color=discord.Color.blue()
      )
      embed.add_field(name="Plant", value="Purchase items from the market.", inline=False)
      embed.add_field(name="Water", value="Sell your items in the market.", inline=False)
      embed.set_footer(text="Use the buttons below to proceed.")

      # Create two buttons
      button1 = Button(label="Plant", style=discord.ButtonStyle.green)
      button2 = Button(label="Water", style=discord.ButtonStyle.blurple)

      # Define what happens when the buttons are clicked
      async def button1_callback(interaction: discord.Interaction):
          logger.info(f"{interaction.user.display_name} clicked the plant button")
          print(f"{interaction.user.display_name} clicked the plant button")

          await interaction.response.send_message("You planted some tomatos in your garden.", ephemeral=True)

      async def button2_callback(interaction: discord.Interaction):
          logger.info(f"{interaction.user.display_name} clicked the water button")
          print(f"{interaction.user.display_name} clicked the water button")
          await interaction.response.send_message("You watered your garden", ephemeral=True)

      # Assign the callback to the buttons
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
      
async def setup(bot):
    await bot.add_cog(GardenCog(bot))      #add_cog(NAME_OF_CLASS(client))   #case sensitive
    