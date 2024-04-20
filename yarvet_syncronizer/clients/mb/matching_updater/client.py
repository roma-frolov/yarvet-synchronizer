import typing

import asyncpg
from loguru import logger

from yarvet_syncronizer.adapters.database.adapter import DBWithRetries
from yarvet_syncronizer.clients.mb.matching_updater.models import Matching


class MatchingUpdater:
    def __init__(self, database: DBWithRetries) -> None:
        self.database: typing.Final[DBWithRetries] = database

    async def batch_update(self, matchings: typing.Sequence[Matching]) -> None:
        for m in matchings:
            is_exists: bool = await self.database.execute(
                "SELECT EXISTS (SELECT 1 FROM common_yarvetproductmatchings WHERE external_id=:external_id)",
                {"external_id": m.id},
            )

            query: str

            if is_exists:
                query = """
                    UPDATE common_yarvetproductmatchings
                    SET article_number=:article_number
                    WHERE external_id=:external_id;
                """
            else:
                query = """
                    INSERT INTO common_yarvetproductmatchings (external_id, article_number)
                    VALUES (:external_id, :article_number);
                """

            values: dict = {
                "external_id": m.id,
                "article_number": m.article_number,
            }

            try:
                await self.database.execute(query, values)
            except asyncpg.UniqueViolationError:
                logger.debug(f"Matching with article_number ='{m.article_number}' already exists")

                await self.database.execute(
                    "DELETE FROM common_yarvetproductmatchings WHERE article_number=:article_number",
                    {"article_number": m.article_number},
                )
                await self.database.execute(query, values)
