### BraxCord Discord Bot
# ButtonsTest.py
# Created: 11/27/24 ~ 7:32pm
# Last Updated: 
# YELLOW HELLO
#############################################################################

import discord
from discord.ext import commands
from discord.ui import Button, View

from discord     import app_commands
import asyncio
import logging
import logging.handlers

logger = logging.getLogger(__name__)


class FarmersMarketCog(commands.Cog):
  """For use with the FarmersMarket. Contains UI element commands"""
  
  def __init__(self, bot):     #bot
    self.bot = bot          #self.bot = bot


  @commands.Cog.listener()    # events use this decorator
  async def on_ready(self):
    print(f"{__name__} is ready!")

  # Set up the bot with a command prefix
  #intents = discord.Intents.default()
  #bot = commands.Bot(command_prefix="!", intents=intents)

  # Define the command
  #@commands.command(name="market")
  #async def market(self, interaction: discord.Interaction):
  @commands.hybrid_command(name="market", description="Create an embed test of the farmers market")
  async def market(self, ctx: commands.Context):
      # Create an embed
      embed = discord.Embed(
          title="Market Actions",
          description="Choose what you want to do in the market:",
          color=discord.Color.blue()
      )
      embed.add_field(name="Buy", value="Purchase items from the market.", inline=False)
      embed.add_field(name="Sell", value="Sell your items in the market.", inline=False)
      embed.set_footer(text="Use the buttons below to proceed.")

      # Create two buttons
      button1 = Button(label="Buy", style=discord.ButtonStyle.green)
      button2 = Button(label="Sell", style=discord.ButtonStyle.red)

      # Define what happens when the buttons are clicked
      async def button1_callback(interaction: discord.Interaction):
          logger.info(f"{interaction.user.display_name} clicked the buy button")
          print(f"{interaction.user.display_name} clicked the buy button")

          await interaction.response.send_message("You clicked the Buy button!", ephemeral=True)

      async def button2_callback(interaction: discord.Interaction):
          logger.info(f"{interaction.user.display_name} clicked the Sell button")
          print(f"{interaction.user.display_name} clicked the sell button")
          await interaction.response.send_message("You clicked the Sell button!", ephemeral=True)

      # Assign the callback to the buttons
      button1.callback = button1_callback
      button2.callback = button2_callback

      # Create a View to hold the buttons
      view = View()
      view.add_item(button1)
      view.add_item(button2)

      # Send Information to the logger and terminal
      logger.info(f"MARKET CALLED\n\tcontext: {ctx}")
      print(f"MARKET CALLED\n\tcontext: {ctx}")


      # Send the message with the embed and buttons
      await ctx.send(embed=embed, view=view)
      
async def setup(bot):
    await bot.add_cog(FarmersMarketCog(bot))      #add_cog(NAME_OF_CLASS(client))   #case sensitive