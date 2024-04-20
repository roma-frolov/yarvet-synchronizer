from decimal import Decimal
from typing import Final

import backoff
from httpx import AsyncClient, HTTPError, Response

from yarvet_syncronizer.clients.response_parsers import check_and_parse_response
from yarvet_syncronizer.clients.yarvet.prices_getter.models import PricesGettingResponse
from yarvet_syncronizer.exceptions import ProductNotFoundError


class PricesGetter:
    def __init__(self, http_client: AsyncClient, token: str) -> None:
        self.http_client: Final[AsyncClient] = http_client
        self.token: Final[str] = token

    @backoff.on_exception(backoff.expo, HTTPError, max_tries=3)
    async def get_price(self, product_id: int) -> Decimal:
        response: Response = await self.http_client.get(
            params={"action": "prices", "token": self.token, "id": product_id},
            url="",
        )
        parsed_response: PricesGettingResponse = check_and_parse_response(
            response=response,
            schema=PricesGettingResponse,
        )

        if not parsed_response.items:
            raise ProductNotFoundError(product_id)

        return parsed_response.items[0].price
