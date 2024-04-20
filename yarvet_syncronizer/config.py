from typing import Annotated, TypeAlias

from pydantic import BeforeValidator, HttpUrl, PostgresDsn, TypeAdapter
from pydantic_settings import BaseSettings


http_url_adapter: TypeAdapter = TypeAdapter(HttpUrl)
Url: TypeAlias = Annotated[str, BeforeValidator(lambda value: str(http_url_adapter.validate_python(value)))]

database_url_adapter: TypeAdapter = TypeAdapter(PostgresDsn)
DbDsn: TypeAlias = Annotated[str, BeforeValidator(lambda value: str(database_url_adapter.validate_python(value)))]


class Settings(BaseSettings):
    yarvet_token: str
    yarvet_url: Url = "https://yarvet.ru/rest/"
    yarvet_timeout: int = 5

    db_dsn: DbDsn
