import aiosqlite

from typing import Optional, Any, Tuple


class Database:
    """
    Class containing methods for interacting with a Database. found in `modules/ext.py`
    
    (Should hopefully take the place of SQLAlchemy for now)
    
    - `_fetch` (static method): multiple modes
        -  `one`
        -  `many`
        -  `all`
    - `connect`: creates a new connection to the database.
    - `execute`: runs query without commits, if `commit` is not passed
        - Use this for fetching commands like `SELECT`
        
    - `run`: runs the query and commits any changes to the database directly.
        - use with commands that modify the db like `CREATE, UPDATE, INSERT, DELETE`, etc.
    
    """
    def __init__(self, db_name: str):
        self.db_name = db_name

    @staticmethod
    async def _fetch(cursor: aiosqlite.Cursor, mode: str) -> Optional[Any]:
        if mode == "one":
            return await cursor.fetchone()
        if mode == "many":
            return await cursor.fetchmany()
        if mode == "all":
            return await cursor.fetchall()

        return None

    async def connect(self) -> aiosqlite.Connection:
        """
        creates a new connection to the database.
        """

        conn = await aiosqlite.connect(self.db_name)
        #conn.row_factory = aiosqlite.Row  # Enables named column access
        return conn   #await aiosqlite.connect(self.db_name)

    async def execute(
        self, query: str, values: Tuple = (), *, fetch: str = None, commit: bool = False,
        conn: aiosqlite.Connection = None
    ) -> Optional[Any]:
        """
        runs the query without committing any changes to the database if `commit` is not passed at func call.

        Tip: use this method for fetching like:`SELECT` queries.

        :param query: SQL query.
        :param values: values to be passed to the query.
        :param fetch: Takes ('one', 'many', 'all').
        :param commit: Commits the changes to the database if it's set to `True`.
        :param conn: pass the new connection to execute two or more methods. If passed, you've to close it manually.
        :return: required data.
        """

        bypass = conn
        conn = await self.connect() if conn is None else conn
        cursor = await conn.cursor()

        await cursor.execute(query, values)
        if fetch is not None:
            data = await self._fetch(cursor, fetch)
        else:
            data = None

        if commit:
            await conn.commit()

        await cursor.close()
        if bypass is None:
            await conn.close()

        return data

    async def run(self, query: str, values: Tuple = (), *, conn: aiosqlite.Connection = None) -> None:
        """
        runs the query and commits any changes to the database directly.

        Tip: use this method if you want to commit changes to the database. Like: `CREATE, UPDATE, INSERT, DELETE`, etc.

        :param query: SQL query
        :param values: values to be passed to the query.
        :param conn: pass the new connection to execute two or more methods. If passed, you've to close it manually.
        """

        await self.execute(query, values, commit=True, conn=conn)
