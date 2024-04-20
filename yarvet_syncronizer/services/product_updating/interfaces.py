import typing
from decimal import Decimal
from typing import Protocol


IWarehouseType = typing.Literal["GLOBAL", "CUSTOM"]


class IStocksGetter(Protocol):
    async def get_stocks(self, product_id: int, warehouse_type: IWarehouseType) -> int: ...


class IPriceGetter(Protocol):
    async def get_price(self, product_id: int) -> Decimal: ...


class IProductUpdater(Protocol):
    async def update(self, product_id: int, stock_quantity: int, price: Decimal) -> None: ...


class IProduct(Protocol):
    id: int
    external_id: int
    warehouse_type: IWarehouseType


class IProductGetter(Protocol):
    async def get_products(self) -> typing.Sequence[IProduct]: ...
