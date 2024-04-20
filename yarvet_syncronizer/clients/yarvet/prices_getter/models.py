from decimal import Decimal

from pydantic import BaseModel, Field


class PriceInfo(BaseModel):
    product_id: int = Field(alias="productId")
    price: Decimal


class PricesGettingResponse(BaseModel):
    items: list[PriceInfo]
