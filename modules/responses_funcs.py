from modules.ext import Database

import aiosqlite
import discord
import logging
import logging.handlers

from typing import Any, Optional


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
logger = logging.getLogger(__name__)


__all__ = [
    "Responses"
]

TABLE_NAME = "responses"  # Enter the table name here (tip:- use only lowercase letters)
columns = ["message_to_detect", "output"]  # You can add more Columns in it !


class Responses:
    def __init__(self, database: Database):
        self._db = database

    async def create_table(self) -> None:
        conn = await self._db.connect()
        await self._db.run(f"CREATE TABLE IF NOT EXISTS `{TABLE_NAME}`(guildID BIGINT, responseID BIGINT, UNIQUE(responseID,guildId))", conn=conn)
        for col in columns:
            try:
                await self._db.run(f"ALTER TABLE `{TABLE_NAME}` ADD COLUMN `{col}` TEXT DEFAULT 0", conn=conn)
            except aiosqlite.OperationalError:
                pass

        await conn.close()


    async def open_resp(self, guild: discord.Guild) -> None:
        #logger.info('open response')
        #print('open response')
        print(f'{__name__}: method: [open_resp]: \tTABLE_NAME: {TABLE_NAME}')

        conn = await self._db.connect()
        data = await self._db.execute(
            f"SELECT responseID, guildID, message_to_detect, output FROM `{TABLE_NAME}` WHERE guildID = ?", (guild.id,),
            fetch="many", conn=conn  # changed to "many" from "one"  # default: one
        )
        print(f'{__name__}: method: [open_resp]:\tdata is {type(data)} type')
        
#        print('attempting loop')
#        for row in data:
#            print(f"responseID: {row[0]}, guildID: {row[1]}, message_to_detect: {row[2]}, output: {row[3]}")
#        print('loop ended')
        #Row
        #iterable[Row]
        
        if data:
            print('{__name__}: method: [open_resp]: [PRINTING LOOP...]')
            for row in data:
                # Assuming `TABLE_NAME` has columns: id, guildID, and some other column `name` for example
                
                print(f"\t- responseID[0]: {row[0]}, guildID[1]: {row[1]}, message_to_detect[2]: {row[2]}, output[3]: {row[3]}")  # Replace with actual columns
                print('{__name__}: method: [open_resp]:\t[END LOOP...]')

        else:
            logger.debug(f"{__name__}: method: [open_resp]:\tNo records found for guildID: {guild.id}")
            print(f"{__name__}: method: [open_resp]:\tNo records found for guildID: {guild.id}")

        
        print(f'{__name__}:\t{data}')



        if data is None:
            print(f'{__name__}: method: [open_resp]:\t`data` is None')
            
            await self._db.run(
                f"INSERT INTO `{TABLE_NAME}`(guildID, responseID, message_to_detect, output) VALUES(?, ?, ?, ?)",
                (guild.id, 1, "Nitro", "https://tenor.com/bP7cy.gif"), conn=conn
            )
        elif data is not None:
                print(f'{__name__}: method: [open_resp]:\tdata is not null!! yay!')
        await conn.close()


    async def get_resp(self, guild: discord.Guild, detect: str) -> Optional[Any]:
        """
        get a single output based on the guild and a detect string. 
        
        Has an overload. swap `detect: str` for `respNum: int`
        
        NOTE: Uses `many` for now. May need to change to `one`
        """
        return await self._db.execute(
            f"SELECT * FROM `{TABLE_NAME}` WHERE guildID = ? AND message_to_detect = ?",
            (guild.id, detect), fetch="many"
        )
        
        
    async def nget_resp(self, guild: discord.Guild, respNum: int) -> Optional[Any]:
        """
        OVERLOAD: get a single output based on the guild and the responseID. 
        
        NOTE: Uses `one` for now.
        """
        return await self._db.execute(
            f"SELECT * FROM `{TABLE_NAME}` WHERE guildID = ? AND responseID = ?",
            (guild.id, respNum), fetch="one"
        )

    async def sget_resp(self, guild: discord.Guild, detect: str) -> Optional[Any]:
        """
        OVERLOAD: get outputs based on the guild and the detect string. 
        
        NOTE: Uses `one` for now.
        """
        return await self._db.execute(
            f"SELECT * FROM `{TABLE_NAME}` WHERE guildID = ? AND message_to_detect = ?",
            (guild.id, detect), fetch="all"
        )
        


    async def get_all_resp(self, guild: discord.Guild) -> Optional[Any]:
        """modified from original get_acc. Gets all responses by Guild"""
        return await self._db.execute(
            f"SELECT * FROM `{TABLE_NAME}` WHERE guildID = ?",
            (guild.id,), fetch="many"
        )
        

    async def update_resp(
        self, guild: discord.Guild, respNum: int = 0, mode: str = "message_to_detect", change: str = "Nitro"
    ) -> Optional[Any]:
        """
        Updates a field in the Responses Table
        
        -----
        **Arguments:**
        
        - `self`
        - `guild: discord.Guild`
            - Used to get the guildID
        - `respNum: int = 0`
            - Used to choose the Response based on ResponseID (the other PK)
            - Defaults to `0` for the first row, if not specified
        - `mode: str`
            - Chooses the column you want to change data in.
            - `"output"` or `"message_to_detect"` are both valid options
            - defaults to `"message_to_detect"`
        - `change: str`
            - Determines what you want to change the data field to.
            - Defaults to `Nitro`
        """
        conn = await self._db.connect()
        data = await self._db.execute(
            f"SELECT * FROM `{TABLE_NAME}` WHERE guildID = ? AND responseID = ?",
            (guild.id, respNum), fetch="one", conn=conn
        )
        if data is not None:
            await self._db.run(
                f"UPDATE `{TABLE_NAME}` SET `{mode}` = `{change}` WHERE guildID = ? AND responseID = ?",
                (guild.id, respNum), conn=conn
            )

        line = await self._db.execute(
            f"SELECT `{mode}` FROM `{TABLE_NAME}` WHERE userID = ? AND responseID = ?",
            (guild.id, respNum), fetch="one", conn=conn
        )

        await conn.close()
        return line




    async def create_resp(
        self, guild: discord.Guild, phrase: str = "Nitro", saythis: str = "nerd"
    ) -> Optional[Any]:
        """
        adds a record in the Responses Table
        
        -----
        **Arguments:**
        
        - `self`
        - `guild: discord.Guild`
            - Used to get the guildID
        - `respNum: int = 0`
            - Used to choose the Response based on ResponseID (the other PK)
            - Defaults to `0` for the first row, if not specified
        - `phrase: str`
            - `message_to_detect` 
            - defaults to `"Nitro"`
        - `saythis: str`
            - `output`
            - Defaults to `nerd`
        """
        conn = await self._db.connect()
        data = await self._db.execute(
            f"SELECT * FROM `{TABLE_NAME}` WHERE guildID = ? AND message_to_detect = ? AND output = ?",
            (guild.id, phrase, saythis), fetch="one", conn=conn
        )
        plus = 0;
        if data is None:
            counter = await self._db.execute(
                f"SELECT count(*) FROM `{TABLE_NAME}` WHERE guildID = ?",
                (guild.id,), fetch="one", conn=conn
            )
            plus = counter[0] + 1
            await self._db.run(
                f"INSERT INTO `{TABLE_NAME}` (responseID, guildID, message_to_detect, output) VALUES (?,?,?,?)",
                (plus, guild.id,phrase,saythis), conn=conn
            )
        else:
            print(f'this response record already exists')
        
        line = await self._db.execute(
            f"SELECT * FROM `{TABLE_NAME}` WHERE guildID = ? AND responseID = ?",
            (guild.id, plus), fetch="one", conn=conn
        )

        await conn.close()
        return line








    async def reset_resp(self, guild: discord.Guild) -> None:
        await self._db.execute(f"DELETE FROM `{TABLE_NAME}` WHERE guildID = ?", (guild.id,))
        await self.open_resp(guild)

    async def get_all_responses(self) -> Any:
        return await self._db.execute(
            f"SELECT `guildID`, `responseID`, `message_to_detect`, `output` FROM `{TABLE_NAME}` ORDER BY `guildID`, `responseID` DESC",
            fetch="all"
        )
