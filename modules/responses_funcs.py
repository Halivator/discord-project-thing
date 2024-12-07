"""responses_funcs.py module

    adapted from Economy Bot's bank_funcs and inventory_funcs modules

    for use by Response.py cog

Returns:
    _type_: _description_
"""

from modules.ext import Database

import aiosqlite
import discord
import logging
import logging.handlers

from typing import Any, Optional


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
logger = logging.getLogger(__name__)


#VERBOSITY
# set if you want to have verbose debug information in the terminal
#debug_v1 = True
#debug_v2 = True
#debug_v3 = True
#
#class Responses_Debug_Settings:
#    """used as a roundabout way to set the debug settings in `__init__.py` to make it easier for other devs to find"""
#    def __init__(self, v1: bool = True, v2: bool = True, v3: bool = True):
#        self._debug_lv_1 = v1
#        self._debug_lv_2 = v2
#        self._debug_lv_3 = v3
#

__all__ = [
    "Responses"
]

TABLE_NAME = "responses"  # Enter the table name here (tip:- use only lowercase letters)
columns = ["message_to_detect", "output"]  # You can add more Columns in it !


class Responses:
    """Class within responses_funcs.py module
    
    for use by Responses.py cog.
    
    Debugging Options:
        **v1** : _**bool**_ \t\t(*Optional*)
        -- **Operations info (i.e. "something happened...")**
        -- Verbosity Level 1 for the terminal window. Enable or Disable certain Print statements
        -- *Default:* `True`
        **v2** : _**bool**_ \t\t(*Optional*)
        -- **loops**
        -- Verbosity Level 2 for the terminal window. Enable or Disable certain Print statements
        -- *Default:* `True`
        **v3** : _**bool**_ \t\t(*Optional*)
        -- **arbitrary info**
        -- Verbosity Level 3 for the terminal window. Enable or Disable certain Print statements
        -- *Default:* `True`
        **v4** : _**bool**_ \t\t(*Optional*)
        -- **Brax info**
        -- Verbosity Level 4 for the terminal window. Enable or Disable certain Print statements
        -- *Default:* `True`
    
    
    Args:
        database (_Database_): database class found in `ext.py`
        
    


    """
    def __init__(self, database: Database, v1: bool = True, v2: bool = True, v3: bool = True, v4: bool = True): #, verbosity: Responses_Debug_Settings):
        self._db = database
        self._v1 = v1   # Operations info (i.e. "something happened...")
        self._v2 = v2   # loops
        self._v3 = v3   # arbitrary info
        self._v4 = v4   # Brax info

    def _v1check(self):
        """Get the status of the cooresponding debugger value to determine what should be printed to terminal.

        To change values, check `modules/__init__.py` and modify the `self.resp = Responses(self)` command

        Returns:
            bool: _v1_ Display Operations info (i.e. "something happened...")
        """
        return self._v1

    def _v2check(self):
        """Get the status of the cooresponding debugger value to determine what should be printed to terminal.

        To change values, check `modules/__init__.py` and modify the `self.resp = Responses(self)` command

        Returns:
            bool: _v2_ Display loops
        """
        return self._v2

    def _v3check(self):
        """Get the status of the cooresponding debugger value to determine what should be printed to terminal.

        To change values, check `modules/__init__.py` and modify the `self.resp = Responses(self)` command

        Returns:
            bool: _v3_ Display arbitrary info
        """
        return self._v3

    def _v4check(self):
        """Get the status of the cooresponding debugger value to determine what should be printed to terminal.

        To change values, check `modules/__init__.py` and modify the `self.resp = Responses(self)` command

        Returns:
            bool: _v4_ Display Brax info
        """
        return self._v4


    async def create_table(self) -> None:
        conn = await self._db.connect()
        await self._db.run(f"CREATE TABLE IF NOT EXISTS `{TABLE_NAME}`(guildID BIGINT, responseID BIGINT, message_to_detect TEXT DEFAULT 0, output TEXT DEFAULT 0, UNIQUE(responseID,guildId,message_to_detect,output))", conn=conn)
        #for col in columns:
        #    try:
        #        await self._db.run(f"ALTER TABLE `{TABLE_NAME}` ADD COLUMN `{col}` TEXT DEFAULT 0", conn=conn)
        #    except aiosqlite.OperationalError:
        #        pass

        await conn.close()


    async def open_resp(self, guild: discord.Guild) -> None:
        #logger.info('open response')
        #print('open response')
        if self._v1: print(f'{__name__}: method: [open_resp]: \tTABLE_NAME: {TABLE_NAME}')

        conn = await self._db.connect()
        data = await self._db.execute(
            f"SELECT responseID, guildID, message_to_detect, output FROM `{TABLE_NAME}` WHERE guildID = ?", (guild.id,),
            fetch="all", conn=conn  # changed to "many" from "one"  # default: one
        )
        if self._v3: print(f'{__name__}: method: [open_resp]:\tdata is {type(data)} type')
        
#        print('attempting loop')
#        for row in data:
#            print(f"responseID: {row[0]}, guildID: {row[1]}, message_to_detect: {row[2]}, output: {row[3]}")
#        print('loop ended')
        #Row
        #iterable[Row]
        
        
        if self._v2 and self._v3:
            if data:
                print(f'{__name__}: method: [open_resp]: [PRINTING LOOP...]')
                for row in data:
                    # Assuming `TABLE_NAME` has columns: id, guildID, and some other column `name` for example
                    
                    print(f"\t- responseID[0]: {row[0]}, guildID[1]: {row[1]}, message_to_detect[2]: {row[2]}, output[3]: {row[3]}")  # Replace with actual columns
                print(f'{__name__}: method: [open_resp]:\t[END LOOP...]')

            else:
                logger.debug(f"{__name__}: method: [open_resp]:\tNo records found for guildID: {guild.id}")
                print(f"{__name__}: method: [open_resp]:\tNo records found for guildID: {guild.id}")

        
        if self._v3:print(f'{__name__}: [open_resp]:\t{data}')



        if data is None:
            # PATH SEEMS TO BE UNLIKELY, AS data COULD BE AN EMPTY LIST
            if self._v1: print(f'{__name__}: method: [open_resp]:\t`data` is None')
            
            await self._db.run(
                f"INSERT INTO `{TABLE_NAME}`(guildID, responseID, message_to_detect, output) VALUES(?, ?, ?, ?)",
                (guild.id, 1, "Nitro", "https://tenor.com/bP7cy.gif"), conn=conn
            )
            await conn.close()


        elif data is not None:
                if self._v3: print(f'{__name__}: method: [open_resp]:\tdata is not null!! yay!')
                
                try:
                    if data[0] is None:
                        print(f'{__name__}: method: [open_resp]:\tdata[0] is null though!!')
                    else:
                        if self._v3: print(f'{data[0]}')
                except:
                    if self._v1: print(f'{__name__}: method: [open_resp]:\tdata[0] was an out of bound index!! Falling back on generating a record for the table')
                    await self._db.run(
                    f"INSERT INTO `{TABLE_NAME}`(guildID, responseID, message_to_detect, output) VALUES(?, ?, ?, ?)",
                    (guild.id, 1, "Nitro", "https://tenor.com/bP7cy.gif"), conn=conn
                )

                await conn.close()
        await conn.close()
        try:
            return data
        except:
            if self._v1: print(f'data not found')
            pass

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
        
        
    async def oget_resp(self, guild: discord.Guild, detect: str, output: str) -> Optional[Any]:
        """
        OVERLOAD: get a single output based on the guild and the responseID. 
        
        NOTE: Uses `one` for now.
        """
        return await self._db.execute(
            f"SELECT * FROM `{TABLE_NAME}` WHERE guildID = ? AND message_to_detect = ? AND output = ?",
            (guild.id, detect, output), fetch="one"
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
        
        NOTE: Uses `all` for now.
        """
        return await self._db.execute(
            f"SELECT * FROM `{TABLE_NAME}` WHERE guildID = ? AND message_to_detect = ?",
            (guild.id, detect), fetch="all"
        )
        


    async def get_all_resp(self, guild: discord.Guild) -> Optional[Any]:
        """modified from original get_acc. Gets all responses by Guild"""
        conn = await self._db.connect()

        
        return await self._db.execute(
            f"SELECT * FROM `{TABLE_NAME}` WHERE guildID = ?",
            (guild.id,), fetch="all", conn = conn
        )
        #data = await self._db.execute(
        #    f"SELECT responseID, guildID, message_to_detect, output FROM `{TABLE_NAME}` WHERE guildID = ?", (guild.id,),
        #    fetch="all", conn=conn  # changed to "many" from "one"  # default: one
        #)

        
    async def get_absolutely_all_resp(self) -> Optional[Any]:
        """
        DO NOT IMPLEMENT OUTSIDE OF TESTING!!!
        
        modified from original get_acc. Gets all responses by Guild
        """
        conn = await self._db.connect()

        return await self._db.execute(
            f"SELECT * FROM `{TABLE_NAME}`",
            (guild.id,), fetch="all", conn = conn
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




    async def s_update_resp(
        self, guild: discord.Guild, phrase: str = "Nitro", saythis: str = "nerd", new_phrase: str = "Nitro", new_saythis: str = "nerd"
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
            f"SELECT * FROM `{TABLE_NAME}` WHERE guildID = ? AND message_to_detect = ? AND output = ?",
            (guild.id, phrase, saythis), fetch="one", conn=conn
        )
        
        temp = 0
        
        if data is not None:
            print(f'\nDATA IS NOT NONE\n')
            temp = data[0]
            
            await self._db.run(
                f"UPDATE `{TABLE_NAME}` SET message_to_detect = ?, output = ? WHERE guildID = ? AND responseID = ?",
                (new_phrase, new_saythis, guild.id, temp), conn=conn
            )



        line = await self._db.execute(
            f"SELECT * FROM `{TABLE_NAME}` WHERE guildID = ? AND responseID = ?",
            (guild.id, temp), fetch="one", conn=conn
        )

        await conn.close()
        return await line



    async def count_resp( self, guild: discord.Guild ) -> Optional[Any]:
        """use this to get the count of responses from an individual guild"""
        conn = await self._db.connect()
        count = 0
        counter = await self._db.execute(
            f"SELECT count(*) FROM `{TABLE_NAME}` WHERE guildID = ?",
            (guild.id,), fetch="one", conn=conn
        )
        count = counter[0]
        return await count

    async def count_all_resp( self, guild: discord.Guild ) -> Optional[Any]:
        """
        DO NOT USE THIS OUTSIDE OF TESTING
        
        use this to get the count of responses from ALL guilds
        """
        conn = await self._db.connect()
        count = 0
        counter = await self._db.execute(
            f"SELECT count(*) FROM `{TABLE_NAME}`",
            (guild.id,), fetch="one", conn=conn
        )
        count = counter[0]
        return await count



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
            line = await self._db.execute(
            f"SELECT `guildID`, `responseID`, `message_to_detect`, `output` FROM `{TABLE_NAME}` WHERE guildID = ? AND responseID = ?",
            (guild.id, plus), fetch="one", conn=conn
            )
        elif data is not None:
            print(f'this response record already exists')
            line = data
        else:
            print(f'lol wut? both is and is not none')
            line = data
        
        

        await conn.close()
        return line





    async def delete_detect_resp(self, guild: discord.Guild, detect: str) -> None:
        await self._db.run(f"DELETE FROM `{TABLE_NAME}` WHERE guildID = ? AND message_to_detect = ?", (guild.id,detect))
        await self.open_resp(guild)

    async def delete_output_resp(self, guild: discord.Guild, detect: str, output:str) -> None:
        await self._db.run(f"DELETE FROM `{TABLE_NAME}` WHERE guildID = ? AND message_to_detect = ? AND output = ?", (guild.id,detect,output))
        await self.open_resp(guild)



    async def reset_resp(self, guild: discord.Guild) -> None:
        await self._db.run(f"DELETE FROM `{TABLE_NAME}` WHERE guildID = ?", (guild.id,))
        await self.open_resp(guild)

    async def get_all_responses(self) -> Any:
        return await self._db.execute(
            f"SELECT `guildID`, `responseID`, `message_to_detect`, `output` FROM `{TABLE_NAME}` ORDER BY `guildID`, `responseID` DESC",
            fetch="all"
        )
