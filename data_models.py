from sqlalchemy import Column, Integer, String, Boolean 
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): 
    pass
   
class User(Base): 
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True), 
    display_name = Column(String), 
    user_handle = Column(String)

class Guild(Base): 
    __tablename__ = "guilds"

    guild_id = Column(Integer, primary_key=True, autoincrement=True)

class UserGuild(Base): 
    __tablename__ = "userguilds"

    user_id = Column(Integer),
    guild_id = Column(Integer)

class Responses(Base): 
    __tablename__ = "responses"

    response_id = Column(Integer, autoincrement=True),
    message_to_detect = Column(String, primary_key=True)
    output = Column(String)

class Garden(Base): 
    __tablename__ = "gardens"

class Wallet(Base): 
    __tablename__ = "wallets"