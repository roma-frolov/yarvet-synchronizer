import typing

from pydantic import BaseModel


class ProductModel(BaseModel):
    id: int
    external_id: int
    warehouse_type: typing.Literal["GLOBAL", "CUSTOM"]
