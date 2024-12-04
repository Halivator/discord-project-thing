#E - File to handle data models and database connection
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

#E Database Setup - for loading database into project
DATABASE_PATH = "sqlite+aiosqlite:///Bot.db"

engine = create_async_engine(DATABASE_PATH, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase): 
    pass
   
class UserGuild(Base): 
    __tablename__ = 'userguilds'

    user_id = Column(Integer, primary_key=True)
    guild_id = Column(Integer, primary_key=True)

class Responses(Base): 
    __tablename__ = 'responses'

    response_id = Column(Integer, autoincrement=True)
    message_to_detect = Column(String, primary_key=True)
    output = Column(String)
    
class Wallet(Base): 
    __tablename__ = 'wallets'

    user_id = Column(String, primary_key=True)
    balance = Column(Integer)
    number_of_tomatoes = Column(Integer)