from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

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