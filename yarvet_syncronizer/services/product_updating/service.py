import typing
from decimal import Decimal
from typing import Final

from yarvet_syncronizer.services.product_updating.interfaces import (
    IPriceGetter,
    IProduct,
    IProductGetter,
    IProductUpdater,
    IStocksGetter,
)


class ProductUpdatingService:
    def __init__(
        self,
        stocks_getter: IStocksGetter,
        price_getter: IPriceGetter,
        product_updater: IProductUpdater,
        product_getter: IProductGetter,
    ) -> None:
        self.stocks_getter: Final[IStocksGetter] = stocks_getter
        self.price_getter: Final[IPriceGetter] = price_getter
        self.product_updater: Final[IProductUpdater] = product_updater
        self.product_getter: Final[IProductGetter] = product_getter

    async def update_products(self) -> None:
        products: typing.Sequence[IProduct] = await self.product_getter.get_products()

        for product in products:
            stocks: int = await self.stocks_getter.get_stocks(
                product_id=product.external_id,
                warehouse_type=product.warehouse_type,
            )
            price: Decimal = await self.price_getter.get_price(product_id=product.external_id)
            await self.product_updater.update(product_id=product.id, stock_quantity=stocks, price=price)
