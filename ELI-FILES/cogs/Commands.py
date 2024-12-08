#E: Shifting commands from main over to a Cog
import discord
from discord import commands
import logging 
from data_models import UserGuild, Responses, Wallet, Base, async_session, initialize_db 
from database_operations import add_to_userguild, get_from_userguild, delete_from_userguild, create_user_wallet, get_user_wallet, update_user_wallet, delete_user_wallet, WalletModel

logger = logging.getLogger(__name__)

class Wallet_Commands(commands.Cog): 

    def __init__(self, client):
        self.client = client

    #E# - https://chatgpt.com/share/6753dcab-f708-8007-ad20-126bc14bcd10 - Chatlog for help debugging and getting resources on using the context(ctx) object
    @commands.command(name='wallet', description="Allow user's to view their wallet's contents") ##Utilizes get_user_wallet and create_user_wallet operations
    async def wallet(self, ctx):
        """Command to display balance and inventory of a user's wallet"""
        """If a user is existing in the server but doesn't have a wallet, create one for them"""
        ##Attributes to create a wallet and address user
        user_id = ctx.author.id 
        name = ctx.author.name 

        #Retrieval of data from WALLETS data table 
        wallet_contents = await get_user_wallet(user_id)

        if wallet_contents: #If the wallet exists, display contents and balance
            balance = wallet_contents.balance 
            tomatoes = wallet_contents.number_of_tomatoes
            await ctx.send(f"💸 {name}, your wallet balance is ${balance}\n You currently have {tomatoes} tomatoes 🍅")
        else: #Otherwise, the wallet doesn't exist, so create one for the user and add it to the database
            initial_balance = 0
            initial_tomatoes = 0
            await create_user_wallet(user_id, initial_balance, initial_tomatoes)
            await ctx.send(f"💯 {name}, your wallet has successfully been created with a balance of ${initial_balance} and inventory of {initial_tomatoes} tomatoes")

    #PORTME
    @commands.command(name='update_balance', description="Allows server administrators to change balance of a user's wallet")
    @commands.has_permissions(administrator=True) #Only allow server admins to interact with this command 
    async def update_wallet_balance(self, ctx, member: discord.Member, new_balance:int): 
        """Update a user's wallet balance - for administrators only"""
        try: 
            updated_wallet = WalletModel(balance=new_balance, number_of_tomatoes=None)

            await update_user_wallet(user_id = member.id, updatedWallet=updated_wallet)
            await ctx.send(f"Successfully updated {member.name}'s balance to {new_balance} 💸") #Success message when user's balance has been updated to db 
        except Exception as ex: 
            await ctx.send(f"An error occurred while trying to update {member.name}'s balance: {str(ex)}") #otherwise display error message to discord

    #PORTME 
    @commands.command(name='update_tomatoes', description="Allow server administrators to change the number of tomatoes a user has in their wallet")
    @commands.has_permissions(administrator=True)
    async def update_user_tomatoes(self, ctx, member:discord.Member, new_tomato_balance:int):
        """Update the number of tomatoes a user has in their inventory - for administrators only"""
        try: 
            updated_wallet = WalletModel(balance=None, number_of_tomatoes=new_tomato_balance)

            await update_user_wallet(user_id=member.id, updatedWallet=updated_wallet)
            await ctx.send(f"Successfully updated {member.name}'s tomato balance to {new_tomato_balance} 🍅") #Success message when user's tomato count has been updated to db
        except Exception as ex: 
            await ctx.send(f"An error occurred while trying to update {member.name}'s wallet: {str(ex)}") #Otherwise display error message to discord

async def setup(client):
    await client.add_cog(Wallet_Commands(client)) #add_cog(NAME_OF_CLASS(client))   #case sensitive