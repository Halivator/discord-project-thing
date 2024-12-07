#from modules import Database

import discord
import os

from discord.ext import commands
from dotenv import load_dotenv, find_dotenv
from pycolorise.colors import *

load_dotenv(find_dotenv(raise_error_if_not_found=True))

__all__ = [
    "Util",
    "Auth"
]


class Util:
    """
    Utility class for helper variables
    
    *Attributes:*
    - `timetick` - `int` tick rate in sec
    """
    timetick = 60
    """tick rate that determines speed of cycling actions (such as status)"""


class Auth:
    """
    Model class that gets Authorized info from the `.env` file.
    
    Make sure to create or request a `.env` if you do not have one in your project root!
    """
    TOKEN = os.getenv("DISCORD_TOKEN")
    """Discord Bot Token. Do not leak!!!"""
    APP_ID = os.getenv("APPLICATION_ID")
    COMMAND_PREFIX = os.getenv("COMMAND_PREFIX")
    """Prefix for text commands"""
    T_GUILD = os.getenv("TEST_GUILD")
    #t_id = int(T_GUILD)
    MY_GUILD = discord.Object(id=int(T_GUILD))
    FILENAME = os.getenv("FILENAME")
    DEV_ID = os.getenv("DEVELOPER_ID")
    """Determines the filename of the .db file"""


