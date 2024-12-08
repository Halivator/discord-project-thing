### BraxCord Discord Bot
# Timer.py
# Created: 12/4/24 ~ 5:39pm
# Last Updated: 12/4/24 
# Code Source: https://chatgpt.com/share/674ce36d-ba44-8002-a0f0-4cc8ceb814de
#############################################################################

import discord
from discord.ext import commands
import asyncio

class TimerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldowns = {}  # Dictionary to track user cooldowns

    @commands.command(name="start_timer")
    async def start_timer(self, ctx, seconds: int):
        """Starts a timer for the user."""
        user = ctx.author

        # Check if the user is already on cooldown
        if user.id in self.cooldowns:
            remaining = self.cooldowns[user.id] - discord.utils.utcnow().timestamp()
            await ctx.send(f"You're still on cooldown! Try again in {int(remaining)} seconds.")
            return

        # Add the user to the cooldown dictionary
        self.cooldowns[user.id] = discord.utils.utcnow().timestamp() + seconds
        await ctx.send(f"Timer started for {seconds} seconds!")

        # Wait for the cooldown to expire
        await asyncio.sleep(seconds)

        # Remove the user from the cooldown dictionary
        del self.cooldowns[user.id]
        await ctx.send(f"Your timer has ended, {user.mention}!")

    @commands.Cog.listener()
    async def on_command(self, ctx):
        """Prevent users on cooldown from running other commands."""
        user = ctx.author

        # Check if the user is on cooldown
        if user.id in self.cooldowns:
            remaining = self.cooldowns[user.id] - discord.utils.utcnow().timestamp()
            if remaining > 0:
                await ctx.send(f"You're on cooldown! Try again in {int(remaining)} seconds.")
                return  # Stop further command execution

# Setup function for the cog
async def setup(bot):
    await bot.add_cog(TimerCog(bot))