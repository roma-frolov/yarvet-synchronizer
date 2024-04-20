import typing

import asyncpg
import backoff
from databases import Database
from databases.core import Transaction


class DBWithRetries:
    def __init__(self, database: Database) -> None:
        self._database: typing.Final[Database] = database

    @backoff.on_exception(backoff.expo, (asyncpg.PostgresConnectionError, OSError), max_tries=3)
    async def fetch_one(self, query: str, values: dict | None = None) -> typing.Any:
        return await self._database.fetch_one(query, values)

    @backoff.on_exception(backoff.expo, (asyncpg.PostgresConnectionError, OSError), max_tries=3)
    async def fetch_val(self, query: str, values: dict | None = None) -> typing.Any:
        return await self._database.fetch_val(query, values)

    @backoff.on_exception(backoff.expo, (asyncpg.PostgresConnectionError, OSError), max_tries=3)
    async def fetch_all(self, query: str, values: dict | None = None) -> typing.Any:
        return await self._database.fetch_all(query, values)

    @backoff.on_exception(backoff.expo, (asyncpg.PostgresConnectionError, OSError), max_tries=3)
    async def execute(self, query: str, values: dict | None = None) -> typing.Any:
        return await self._database.execute(query, values)

    @backoff.on_exception(backoff.expo, (asyncpg.PostgresConnectionError, OSError), max_tries=3)
    def transaction(self, *, force_rollback: bool = False, **kwargs: typing.Any) -> Transaction:
        return self._database.transaction(force_rollback=force_rollback, **kwargs)

    @backoff.on_exception(backoff.expo, (asyncpg.PostgresConnectionError, OSError), max_tries=3)
    async def execute_many(self, query: str, values: list[dict]) -> typing.Any:
        return await self._database.execute_many(query, values)
