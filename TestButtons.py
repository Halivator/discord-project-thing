### BraxCord Discord Bot
# ButtonsTest.py
# Created: 11/27/24 ~ 7:32pm
# Last Updated: 12/1/24 
# Code Source: ChatGPT - https://chatgpt.com/share/674ce36d-ba44-8002-a0f0-4cc8ceb814de
#############################################################################

import discord
from discord.ext import commands
from discord.ui import Button, View

class FarmersMarketCog(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()    # events use this decorator
  async def on_ready(self):
    print("market.py is ready!")

  # Set up the bot with a command prefix
  intents = discord.Intents.default()
  bot = commands.Bot(command_prefix="!", intents=intents)

  # Define the command
  @bot.command(name="market")
  async def market(ctx):
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
      async def button1_callback(interaction):
          await interaction.response.send_message("You clicked the Buy button!", ephemeral=True)

      async def button2_callback(interaction):
          await interaction.response.send_message("You clicked the Sell button!", ephemeral=True)

      # Assign the callback to the buttons
      button1.callback = button1_callback
      button2.callback = button2_callback

      # Create a View to hold the buttons
      view = View()
      view.add_item(button1)
      view.add_item(button2)

      # Send the message with the embed and buttons
      await ctx.send(embed=embed, view=view)