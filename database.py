from dotenv import load_dotenv
import discord
import os 

import sqlite3



database = sqlite3.connect('database.db')
cursor = database.cursor()
database.execute("CREATE TABLE IF NOT EXISTS messages(message_content STRING, message_id INTEGER)")  # Create a table if it does not already exist