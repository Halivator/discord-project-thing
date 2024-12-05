#E - File for CRUD operations on Database & database data management
#https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
from data_models import UserGuild, Wallet, Responses, Base, async_session
from discord import HTTPException
from pydantic import BaseModel

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
async def get_from_userguild(user_id: int): 
    async with async_session() as db_session: 
        userguild_to_get = db_session.query(UserGuild).filter(UserGuild.user_id == user_id).first()

        return userguild_to_get

#DELETE 
async def delete_from_userguild(user_id: int): 
    async with async_session() as db_session: 
        userguild_to_delete = await db_session.get(UserGuild, user_id)

        if not userguild_to_delete: 
            raise HTTPException(response="User guild relationship not found", status=400)
        
        await db_session.delete(userguild_to_delete)
        await db_session.commit()
        return True

#Set of CRUD operations for wallets table 
#CREATE
async def create_user_wallet(user_id: int, balance: int, number_of_tomatoes: int):  
    async with async_session() as db_session: 
        new_wallet = Wallet(user_id=user_id, balance=balance, number_of_tomatoes=number_of_tomatoes)
        db_session.add(new_wallet)
        await db_session.commit() 
        return new_wallet

#READ
async def get_user_wallet(): ##model similarly to get_userguild
    pass

#UPDATE
async def update_user_wallet(user_id: int, updatedWallet:WalletModel):
     async with async_session() as db_session: 
        wallet = db_session.query(Wallet).filter(Wallet.user_id == user_id).first() #ensure the user ID matches an id in the db 

        if not wallet: 
            raise HTTPException(response="Wallet not found, cannot update inventory", status=404)
    
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
            raise HTTPException(response = "User wallet not found, cannot be deleted", status=404)
        
    await db_session.delete(wallet_to_delete)
    await db_session.commit() 

