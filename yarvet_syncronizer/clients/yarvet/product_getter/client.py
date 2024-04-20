from typing import Final

import backoff
from httpx import AsyncClient, HTTPError, Response

from yarvet_syncronizer.clients.response_parsers import check_and_parse_response
from yarvet_syncronizer.clients.yarvet.product_getter.models import MatchingModel, ProductsGettingResponse


class ProductGetter:
    def __init__(self, http_client: AsyncClient, token: str) -> None:
        self.http_client: Final[AsyncClient] = http_client
        self.token: Final[str] = token

    @backoff.on_exception(backoff.expo, HTTPError, max_tries=3)
    async def get_matchings_of_ids_to_articles(self) -> list[MatchingModel]:
        response: Response = await self.http_client.get(
            params={"action": "products", "token": self.token},
            url="",
        )
        parsed_response: ProductsGettingResponse = check_and_parse_response(
            response=response,
            schema=ProductsGettingResponse,
        )

        matchings: list[MatchingModel] = parsed_response.items

        request_number: int = 2

        while request_number <= parsed_response.pages:
            response = await self.http_client.get(
                params={"action": "products", "token": self.token, "page": request_number},
                url="",
            )

            parsed_response = check_and_parse_response(
                response=response,
                schema=ProductsGettingResponse,
            )

            matchings.extend(parsed_response.items)
            request_number += 1

        return matchings
