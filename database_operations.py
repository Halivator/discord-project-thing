#E - File for CRUD operations on Database & database data management
from data_models import UserGuild, Wallet, Responses, Base, async_session

#Set of CRUD operations for userguilds table
#CREATE
async def add_to_userguild(user_id: int, guild_id: int, guild_name: str): 
    async with async_session() as db_session: 
        new_userguild = UserGuild(user_id = user_id, guild_id=guild_id, guild_name=guild_name)
        db_session.add(new_userguild)
        await db_session.commit()
        return new_userguild

#READ 
async def get_from_userguild(): 
    pass 

#UPDATE 
async def update_userguild(): 
    pass 

#DELETE 
async def delete_from_userguild(): 
    pass

#Set of CRUD operations for wallets table 
#CREATE
async def create_user_wallet(): 
    pass

#READ
async def get_user_wallet(): 
    pass 

#UPDATE
async def update_user_wallet():
    pass 

#DELETE
async def delete_from_user_wallet(): 
    pass 



