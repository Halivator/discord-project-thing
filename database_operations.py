#E - File for CRUD operations on Database & database data management
#https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
#https://medium.com/@shubhkarmanrathore/mastering-crud-operations-with-sqlalchemy-a-comprehensive-guide-a05cf70e5dea
from data_models import UserGuild, Wallet, async_session
from discord import HTTPException
from pydantic import BaseModel
from sqlalchemy import delete
from sqlalchemy.future import select #-https://docs.sqlalchemy.org/en/14/core/future.html

class WalletModel(BaseModel): 
    balance: int
    number_of_tomatoes: int

    class Config: 
        orm_mode=True

#Set of CRUD operations for userguilds table
#CREATE
async def add_to_userguild(user_id: int, guild_id: int, guild_name: str): 
    async with async_session() as db_session: 
        new_userguild = UserGuild(user_id=user_id, guild_id=guild_id, guild_name=guild_name)
        db_session.add(new_userguild)
        await db_session.commit()
        return new_userguild

#READ 
#Get by a user's ID
#Review these (get wallet) - not sure it will work exactly the same was as for P1
async def get_from_userguild(user_id: int): 
    try: #Adding exception handling for logging just in case this doesn't work as expected
        async with async_session() as db_session: 
            userguild_to_get = await db_session.query(UserGuild).filter(UserGuild.user_id == user_id).first()
            return userguild_to_get
    except Exception as e: #Similar to try-catch in C#
        print("User, {user_id}, is not found in any servers. Cannot be retrieved.") #Print to termimal
        return None

#DELETE 
async def delete_from_userguild(guild_id: int): 
    async with async_session() as db_session: 
        userguild_records_to_delete = await db_session.execute(
            delete(UserGuild).filter(UserGuild.guild_id == guild_id) #Fetch and directly delete records with a matching guild_id
        )
       
        await db_session.commit() #commit delete transaction
        return userguild_records_to_delete.rowcount()

#Set of CRUD operations for wallets table 
#CREATE
async def create_user_wallet(user_id: int, balance: int, number_of_tomatoes: int):  
    async with async_session() as db_session: 
        new_wallet = Wallet(user_id=user_id, balance=balance, number_of_tomatoes=number_of_tomatoes)
        db_session.add(new_wallet)
        await db_session.commit() 
        return new_wallet

#READ
#Get by a user's ID
async def get_user_wallet(user_id: int): 
    try: 
        async with async_session() as db_session: 
            wallet_to_get = await db_session.query(Wallet).filter(Wallet.user_id == user_id).first()
            return wallet_to_get
    except Exception as e: 
        print("Wallet for user {user_id} cannot be retrieved: it either doesn't exsist, or entry was invalid.") #print to terminal
        return None

#UPDATE
async def update_user_wallet(user_id: int, updatedWallet:WalletModel):
     async with async_session() as db_session: 
        wallet = db_session.query(Wallet).filter(Wallet.user_id == user_id).first() #ensure the user ID matches an id in the db 

        if not wallet: 
            raise HTTPException(response="Wallet not found, cannot update inventory", status=404) #display to terminal
    
    #assign each of the updated attributes 
        wallet.balance = updatedWallet.balance
        wallet.number_of_tomatoes = updatedWallet.number_of_tomatoes

        await db_session.commit() #commit the changes to DB 
        await db_session.refresh(wallet) #refresh the attributes of the updated user

#DELETE
async def delete_from_user_wallet(user_id: int): 
    async with async_session as db_session: 
        wallet_to_delete = await db_session.get(Wallet, user_id)

        if not wallet_to_delete: 
            raise HTTPException(response = "User wallet not found, cannot be deleted", status=404) #display to terminal
        
    await db_session.delete(wallet_to_delete)
    await db_session.commit() 

