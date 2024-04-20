import typing

from yarvet_syncronizer.adapters.database.adapter import DBWithRetries
from yarvet_syncronizer.clients.mb.product_getter.models import ProductModel


class ProductGetter:
    def __init__(self, database: DBWithRetries) -> None:
        self.database: typing.Final[DBWithRetries] = database

    async def get_products(self) -> typing.Sequence[ProductModel]:
        query: str = """
            SELECT p.id, w.type warehouse_type, ypm.external_id
            FROM provider_product p
            JOIN common_warehouse w ON p.warehouse_id = w.id
            JOIN common_yarvetproductmatchings ypm ON p.product_code = ypm.article_number;
        """
        raw_products: list[typing.Mapping] = await self.database.fetch_all(query)

        return [ProductModel(**dict(p)) for p in raw_products]
