import typing

from pydantic import BaseModel, Field


class StockInfo(BaseModel):
    product_id: int = Field(alias="productId")
    main_store: int = Field(alias="mainStore")
    user_store: int = Field(alias="userStore")


class StocksGettingResponse(BaseModel):
    items: list[StockInfo]


WarehouseType = typing.Literal["GLOBAL", "CUSTOM"]
