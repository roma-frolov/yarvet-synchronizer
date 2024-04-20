from typing import Literal

from pydantic import BaseModel


class Product(BaseModel):
    id: int
    warehouse_type: Literal["GLOBAL", "CUSTOM"]
