#E: Shifting commands from main over to a Cog
import discord
from discord.ext import commands
import logging 
from data_models import UserGuild, Responses, Wallet, Base, async_session, initialize_db 
from database_operations import add_to_userguild, get_from_userguild, delete_from_userguild, create_user_wallet, get_user_wallet, update_user_wallet, delete_user_wallet, WalletModel

logger = logging.getLogger(__name__)

class WalletCommands(commands.Cog): 

    def __init__(self, client):
        self.client = client

    #E# - https://chatgpt.com/share/6753dcab-f708-8007-ad20-126bc14bcd10 - Chatlog for help debugging and getting resources on using the context(ctx) object
    @commands.guild_only()
    @commands.command(name='wallet', description="Allow user's to view their wallet's contents") ##Utilizes get_user_wallet and create_user_wallet operations
    async def wallet(self, ctx, member: discord.Member = None):
        """Command to display balance and inventory of a user's wallet"""
        """If a user is existing in the server but doesn't have a wallet, create one for them"""
        ##Attributes to create a wallet and address user
        member = member or ctx.author
        user_id = member.id
        name = member.name

        #Retrieval of data from WALLETS data table 
        wallet_contents = await get_user_wallet(user_id)

        if wallet_contents: #If the wallet exists, display contents and balance
            balance = wallet_contents.balance 
            tomatoes = wallet_contents.number_of_tomatoes
            if member == ctx.author:  ##If the author is the one checking their wallet
                await ctx.send(f"💸 {name}, your wallet balance is ${balance}\n You currently have {tomatoes} tomatoes 🍅")
            else: ##If the author is checking another user's balance
                await ctx.send(f"{name}'s wallet balance is ${balance}\nThey currently have {tomatoes} tomatoes 🍅")
        else: #Otherwise, the wallet doesn't exist, so create one for the user and add it to the database
            if member == ctx.author: 
                initial_balance = 500
                initial_tomatoes = 0
                await create_user_wallet(user_id, initial_balance, initial_tomatoes)
                await ctx.send(f"💯 {name}, your wallet has successfully been created with a balance of ${initial_balance} and inventory of {initial_tomatoes} tomatoes")
            else: ##IF user does not have wallet created
                await ctx.send(f"User does not currently have a wallet! They need to run the '!wallet' command! ❌👛")

    @commands.guild_only()
    @commands.command(name='update_balance', description="Allows server administrators to change balance of a user's wallet")
    @commands.has_permissions(administrator=True) #Only allow server admins to interact with this command 
    async def update_wallet_balance(self, ctx, member: discord.Member, new_balance:int): 
        """Update a user's wallet balance - for administrators only"""
        try: 
            try:
                starting_wallet = await get_user_wallet(member.id)
            except Exception as ex: 
                await ctx.send(f"Inner error when trying to make a temporary wallet. An error occurred while trying to get {member.name}'s balance: {str(ex)}") #otherwise display error message to discord
            updated_wallet = WalletModel(balance=new_balance, number_of_tomatoes=starting_wallet.number_of_tomatoes)
            #updated_wallet = WalletModel(balance=new_balance, number_of_tomatoes=starting_wallet.number_of_tomatoes)

            await update_user_wallet(user_id = member.id, updatedWallet=updated_wallet)
            await ctx.send(f"Successfully updated {member.name}'s balance to {new_balance} 💸") #Success message when user's balance has been updated to db 
        except Exception as ex: 
            await ctx.send(f"An error occurred while trying to update {member.name}'s balance: {str(ex)}") #otherwise display error message to discord
 
    @commands.guild_only()
    @commands.command(name='update_tomatoes', description="Allow server administrators to change the number of tomatoes a user has in their wallet")
    @commands.has_permissions(administrator=True)
    async def update_user_tomatoes(self, ctx, member:discord.Member, new_tomato_balance:int):
        """Update the number of tomatoes a user has in their inventory - for administrators only"""
        try: 
            try:
                starting_wallet = await get_user_wallet(member.id)
            except Exception as ex: 
                await ctx.send(f"Inner error when trying to make a temporary wallet. An error occurred while trying to get {member.name}'s wallet: {str(ex)}") #Otherwise display error message to discord
            updated_wallet = WalletModel(balance=starting_wallet.balance, number_of_tomatoes=new_tomato_balance)
            #updated_wallet = WalletModel(balance=starting_wallet.balance, number_of_tomatoes=new_tomato_balance)

            await update_user_wallet(user_id=member.id, updatedWallet=updated_wallet)
            await ctx.send(f"Successfully updated {member.name}'s tomato balance to {new_tomato_balance} 🍅") #Success message when user's tomato count has been updated to db
        except Exception as ex: 
            await ctx.send(f"An error occurred while trying to update {member.name}'s wallet: {str(ex)}") #Otherwise display error message to discord


    # ported over from Eli's main `@bot.event` events
    @commands.Cog.listener("on_member_join")
    @commands.guild_only()
    async def make_wallet_on_join(self, member: discord.Member):
        """When a member joins the server, create their wallet (utilizes create_user_wallet)"""
        wallet_created = await create_user_wallet(user_id=member.id, initial_balance=500, starting_number_of_tomatoes=0)
        if wallet_created: 
            print(f"[{__name__}]\t[ EVENT ]: on_member_join:\tThe wallet was successfully created for {member.name} : {member.id}") #Print to terminal, since this happens by default, user does not need to see this message
        else: 
            print(f"[{__name__}]\t[ EVENT ]: on_member_join:\tThere was an error creating the wallet for {member.name} : {member.id}, or, a wallet already exists for this user")

    # ported over from Eli's main `@bot.event` events
    @commands.Cog.listener("on_guild_remove")
    @commands.guild_only()
    async def remove_users_on_guild_remove(self, guild: discord.Guild): 
        """When the bot has been removed from the server, get rid of data stored by the bot"""
        removal_count = await delete_from_userguild(guild_id=guild.id) #Remove from UserGuild table where guild_ids match

        if removal_count > 0: 
            print(f"[{__name__}]\t[ EVENT ]: on_guild_remove\tSuccessfully removed records for {guild.name} : {guild.id} from UserGuilds") ##For logging & testing
        else: 
            print(f"[{__name__}]\t[ EVENT ]: on_guild_remove\tError removing records for {guild.name} : {guild.id} from UserGuilds")

    # ported over from Eli's main `@bot.event` events
    @commands.Cog.listener("on_member_remove")
    @commands.guild_only()
    async def remove_wallet_on_member_remove(self, member: discord.Member): 
        """When a member leaves the server, remove their wallet (utilizes delete_user_wallet)"""
        wallet_deleted = await delete_user_wallet(user_id=member.id)
        if wallet_deleted: 
            print(f"[{__name__}]\t[ EVENT ]: on_member_remove\tThe wallet for user {member.name} : {member.id} has been successfully removed.")
        else: 
            print(f"[{__name__}]\t[ EVENT ]: on_member_remove\tThe wallet for user {member.name} could not be deleted, or was not found.")

async def setup(client):
    await client.add_cog(WalletCommands(client)) #add_cog(NAME_OF_CLASS(client))   #case sensitive
