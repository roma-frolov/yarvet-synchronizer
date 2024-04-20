import typing
from decimal import Decimal

from yarvet_syncronizer.adapters.database.adapter import DBWithRetries


class ProductUpdater:
    def __init__(self, database: DBWithRetries) -> None:
        self.database: typing.Final[DBWithRetries] = database

    async def update(self, product_id: int, stock_quantity: int, price: Decimal) -> None:
        query: str = """
            UPDATE provider_product
            SET stock_quantity=:stock_quantity, price=:price, discounted_price=:price
            WHERE id=:id;
        """

        values: dict = {
            "stock_quantity": stock_quantity,
            "price": price,
            "id": product_id,
        }

        await self.database.execute(query, values)
