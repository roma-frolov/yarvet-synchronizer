from pydantic import BaseModel, Field


class MatchingModel(BaseModel):
    id: int
    article_number: str = Field(alias="articleNumber")


class ProductsGettingResponse(BaseModel):
    pages: int
    current_page: int = Field(alias="curPage")
    items: list[MatchingModel]
