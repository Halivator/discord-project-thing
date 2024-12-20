# Incorporated from https://gist.github.com/bynect/2d7317b4e2a3e926f2ce392e5e7cca4b

from discord.ext import commands
import discord
from sys import version_info as sysv
from os import listdir

import sys
sys.path.append("..")

from base import Auth

class Dev(commands.Cog):
	"""This is a cog with owner-only commands.
	Note:
		All cogs inherits from `commands.Cog`_.
		All cogs are classes, so they need self as first argument in their methods.
		All cogs use different decorators for commands and events (see example below).
		All cogs needs a setup function (see below).
    Documentation:
        https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html
	"""
	def __init__(self, bot):
		self.bot = bot



	def dev_check():
		async def predicate(ctx):
			chk = False
			print(f'author id:\t{ctx.message.author.id}')
			print(f'dev id:\t\t{Auth.DEV_ID}')
			author = int(ctx.message.author.id)
			dev = int(Auth.DEV_ID)
			if author == dev:
				chk = True
				print(f'{chk}')
			return chk
		return commands.check(predicate)
    
#	def second_check():
#		async def predicate(ctx):
#			chk = False
#			print(f'author id:\t{ctx.message.author.id}')
#			print(f'dev id:\t\t{Auth.DEV_ID}')
#			author = int(ctx.message.author.id)
#			dev = int(Auth.DEV_ID)
#			if author != dev:
#				chk = True
#			print(f'{chk}')
#			return chk
#		return commands.check(predicate)


 
 
	@commands.Cog.listener()
	#This is the decorator for events (inside of cogs).
	async def on_ready(self):
		print(f'Python {sysv.major}.{sysv.minor}.{sysv.micro} - Disord.py {discord.__version__}\n')
		#Prints on the shell the version of Python and Discord.py installed in our computer.


	@commands.command(name='reloadall', hidden=True)#This command is hidden from the help menu.
	#This is the decorator for commands (inside of cogs).
 	#@commands.is_owner()
	@commands.check_any(commands.is_owner(), dev_check())
	#Only the owner (or owners) can use the commands decorated with this.
	async def reload_all(self, ctx):
		"""This commands reloads all the cogs in the `./cogs` folder.
		
		Note:
			This command can be used only from the bot owner.
			This command is hidden from the help menu.
			This command deletes its messages after 20 seconds."""

		message = await ctx.send('Reloading...')
		ct = ""
		works = False
		try:
			await ctx.message.delete()
			works = True
		except Exception as exc:
			ct = f'An error has occurred: {exc}'
		try:
			for cog in listdir('./cogs'):
				if cog.endswith('.py') == True:
					self.bot.reload_extension(f'cogs.{cog[:-3]}')
		except Exception as exc:
			await message.edit(content=f'An error has occurred: {exc}', delete_after=20)
		else:
			await message.edit(content='All cogs have been reloaded.', delete_after=20)
		if works == False:
			await ctx.send(f"{ct}", delete_after=25, silent=True)


	def check_cog(self, cog):
		"""Returns the name of the cog in the correct format.
		Args:
			self
			cog (str): The cogname to check
		
		Returns:
			cog if cog starts with `cogs.`, otherwise an fstring with this format`cogs.{cog}`_.
		Note:
			All cognames are made lowercase with `.lower()`_.
		"""
		if (cog.lower()).startswith('cogs.') == True:
			return cog.lower()
		return f'cogs.{cog.lower()}'

	@commands.command(name='load', hidden=True)
	@commands.check_any(commands.is_owner(), dev_check())	
	async def load_cog(self, ctx, *, cog: str):
		"""This commands loads the selected cog, as long as that cog is in the `./cogs` folder.
				
		Args:
			cog (str): The name of the cog to load. The name is checked with `.check_cog(cog)`_.
		
		Note:
			This command can be used only from the bot owner.
			This command is hidden from the help menu.
			This command deletes its messages after 20 seconds.
		"""
		message = await ctx.send('Loading...')
		ct = ""
		works = False
		try:
			await ctx.message.delete()
			works = True
		except Exception as exc:
			ct = f'An error has occurred: {exc}'
		try:
			self.bot.load_extension(self.check_cog(cog))
		except Exception as exc:
			await message.edit(content=f'An error has occurred: {exc}', delete_after=20)
		else:
			await message.edit(content=f'{self.check_cog(cog)} has been loaded.', delete_after=20)
		if works == False:
			await ctx.send(f"{ct}", delete_after=25, silent=True)





	@commands.command(name='unload', hidden=True)
	@commands.check_any(commands.is_owner(), dev_check())	
	async def unload_cog(self, ctx, *, cog: str):
		"""This commands unloads the selected cog, as long as that cog is in the `./cogs` folder.
		
		Args:
			cog (str): The name of the cog to unload. The name is checked with `.check_cog(cog)`_.
		Note:
			This command can be used only from the bot owner.
			This command is hidden from the help menu.
			This command deletes its messages after 20 seconds.
		"""
		message = await ctx.send('Unloading...')
		ct = ""
		works = False
		try:
			await ctx.message.delete()
			works = True
		except Exception as exc:
			ct = f'An error has occurred: {exc}'
		try:
			self.bot.unload_extension(self.check_cog(cog))
		except Exception as exc:
			await message.edit(content=f'An error has occurred: {exc}', delete_after=20)
		else:
			await message.edit(content=f'{self.check_cog(cog)} has been unloaded.', delete_after=20)
		if works == False:
			await ctx.send(f"{ct}", delete_after=25, silent=True)







	@commands.command(name='reload', hidden=True)
	@commands.check_any(commands.is_owner(), dev_check())	
	async def reload_cog(self, ctx, *, cog: str):
		"""This commands reloads the selected cog, as long as that cog is in the `./cogs` folder.
		
		Args:
			cog (str): The name of the cog to reload. The name is checked with `.check_cog(cog)`_.
		Note:
			This command can be used only from the bot owner.
			This command is hidden from the help menu.
			This command deletes its messages after 20 seconds.
		"""
		message = await ctx.send('Reloading...')
		ct = ""
		works = False
		try:
			await ctx.message.delete()
			works = True
		except Exception as exc:
			ct = f'An error has occurred: {exc}'

		try:
			self.bot.reload_extension(self.check_cog(cog))
		except Exception as exc:
			await message.edit(content=f'An error has occurred: {exc}', delete_after=20)
		else:
			await message.edit(content=f'{self.check_cog(cog)} has been reloaded.', delete_after=20)
		if works == False:
			await ctx.send(f"{ct}", delete_after=25, silent=True)



async def setup(bot):
	"""Every cog needs a setup function like this."""
	await bot.add_cog(Dev(bot))
 
 
 
 
 
 
 
 ## Added the following to account for missing `manage_messages` permissions
##	Replaces message.deleted()
# 		ct = ""
#		works = False
#		try:
#			await ctx.message.delete()
#			works = True
#		except Exception as exc:
#			await ct = f'An error has occurred: {exc}'

##  Goes after the result of the commands
#		if works == False:
#			await ctx.send(f"{ct}", delete_after=25, silent=True)

