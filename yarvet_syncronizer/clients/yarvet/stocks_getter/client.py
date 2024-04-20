from typing import Final

import backoff
from httpx import AsyncClient, HTTPError, Response

from yarvet_syncronizer.clients.response_parsers import check_and_parse_response
from yarvet_syncronizer.clients.yarvet.stocks_getter.models import StockInfo, StocksGettingResponse, WarehouseType
from yarvet_syncronizer.exceptions import ProductNotFoundError


class StocksGetter:
    def __init__(self, http_client: AsyncClient, token: str) -> None:
        self.http_client: Final[AsyncClient] = http_client
        self.token: Final[str] = token

    @backoff.on_exception(backoff.expo, HTTPError, max_tries=3)
    async def get_stocks(self, product_id: int, warehouse_type: WarehouseType) -> int:
        response: Response = await self.http_client.get(
            params={"action": "quantities", "token": self.token, "id": product_id},
            url="",
        )
        parsed_response: StocksGettingResponse = check_and_parse_response(
            response=response,
            schema=StocksGettingResponse,
        )

        if not parsed_response.items:
            raise ProductNotFoundError(product_id)

        stocks_info: StockInfo = parsed_response.items[0]

        stocks: int = stocks_info.main_store if warehouse_type == "GLOBAL" else stocks_info.user_store

        return stocks
