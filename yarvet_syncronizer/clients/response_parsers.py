import json
import logging
from typing import TypeVar

from httpx import HTTPStatusError, Response


T = TypeVar("T")


def check_and_parse_response(*, response: Response, schema: type[T]) -> T:
    check_response_http_error(response)
    return parse_single(response, schema)


def check_and_parse_response_list(*, response: Response, schema: type[T]) -> list[T]:
    check_response_http_error(response)
    return parse_list(response, schema)


def check_response_http_error(response: Response) -> None:
    try:
        response.raise_for_status()
    except HTTPStatusError as exc:
        logging.exception(f"Response HttpError response_text={exc.response.text}")
        raise


def parse_single(response: Response, schema: type[T]) -> T:
    response_json: dict | list = check_response_json_error(response)

    try:
        return schema(**response.json())
    except (ValueError, TypeError):
        logging.exception(f"Response parsing error {response_json=}")
        raise


def parse_list(response: Response, schema: type[T]) -> list[T]:
    response_json: dict | list = check_response_json_error(response)

    try:
        return [schema(**data) for data in response_json]
    except (ValueError, TypeError):
        logging.exception(f"Response parsing error {response_json=}")
        raise


def check_response_json_error(response: Response) -> dict | list:
    try:
        return response.json()
    except json.decoder.JSONDecodeError:
        logging.exception(f"Response HttpError response_text={response.text}")
        raise
