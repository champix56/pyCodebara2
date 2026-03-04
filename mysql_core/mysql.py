import aiomysql
from typing import Any, List, Optional, Tuple
import asyncio

import os
"""
DB_HOST = os.getenv("DB_HOST", "mysql")  # doit être 'mysql', pas 'localhost'
DB_PORT = int(os.getenv("DB_PORT", 3306))
"""
DB_HOST = '127.0.0.1'
DB_PORT = 3306

class MySQLClient:
    """
    Client MySQL async (PROD, non bloquant)
    """

    def __init__(
        self,
        host: str = DB_HOST,
        user: str = "champix",
        password: str = "alex",
        database: str = "cdb",
        port: int = DB_PORT,
        minsize: int = 1,
        maxsize: int = 10
    ):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.minsize = minsize
        self.maxsize = maxsize

        self._pool: Optional[aiomysql.Pool] = None

    # ======================================================
    # CONNECTION POOL
    # ======================================================

    async def connect(self):
        """
        Initialise le pool de connexions MySQL
        """
        if self._pool is None:
            self._pool = await aiomysql.create_pool(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db=self.database,
                minsize=self.minsize,
                maxsize=self.maxsize,
                autocommit=True
            )

    async def close(self):
        """
        Ferme le pool proprement
        """
        if self._pool:
            self._pool.close()
            await self._pool.wait_closed()
            self._pool = None

    # ======================================================
    # QUERY EXECUTION
    # ======================================================

    async def execute(
        self,
        query: str,
        params: Optional[Tuple[Any, ...]] = None
    ) -> List[dict]:
        """
        Exécute une requête SQL et retourne le résultat

        - SELECT → liste de dict
        - INSERT/UPDATE/DELETE → liste vide
        """
        if self._pool is None:
            raise RuntimeError("MySQL pool not initialized. Call connect() first.")
        else:
            print('connected')
        async with self._pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, params or ())
                if cursor.description:
                    return await cursor.fetchall()
                else:
                    print('empty')
                return []
    async def nonQuery(self,query:str,params=None):
        if self._pool is None:
            raise RuntimeError("MySQL pool not initialized. Call connect() first.")
        else:
            print('connected')
        async with self._pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, params or ())
                await conn.commit()
