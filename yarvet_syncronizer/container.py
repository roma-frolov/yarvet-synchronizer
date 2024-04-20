from bakery import Bakery, Cake
from databases import Database
from httpx import AsyncClient

from yarvet_syncronizer.adapters.database.adapter import DBWithRetries
from yarvet_syncronizer.clients.mb.matching_updater.client import MatchingUpdater
from yarvet_syncronizer.clients.mb.product_getter.client import ProductGetter
from yarvet_syncronizer.clients.mb.product_updater.client import ProductUpdater
from yarvet_syncronizer.clients.yarvet.prices_getter.client import PricesGetter
from yarvet_syncronizer.clients.yarvet.product_getter.client import ProductGetter as YarvetProductGetter
from yarvet_syncronizer.clients.yarvet.stocks_getter.client import StocksGetter
from yarvet_syncronizer.config import Settings
from yarvet_syncronizer.services.load_matching.service import LoadMatchingService
from yarvet_syncronizer.services.product_updating.service import ProductUpdatingService


class Container(Bakery):
    config: Settings = Cake(Settings)  # type: ignore[assignment]
    _yarvet_http_client: AsyncClient = Cake(AsyncClient, base_url=config.yarvet_url, timeout=config.yarvet_timeout)

    _database_no_retries: Database = Cake(
        Cake(
            Database,
            url=config.db_dsn,
        ),
    )

    _database: DBWithRetries = Cake(DBWithRetries, _database_no_retries)

    _yarvet_stocks_getter: StocksGetter = Cake(StocksGetter, http_client=_yarvet_http_client, token=config.yarvet_token)
    _yarvet_prices_getter: PricesGetter = Cake(PricesGetter, http_client=_yarvet_http_client, token=config.yarvet_token)
    _yarvet_product_getter: YarvetProductGetter = Cake(
        YarvetProductGetter,
        http_client=_yarvet_http_client,
        token=config.yarvet_token,
    )

    _mb_product_updater: ProductUpdater = Cake(ProductUpdater, database=_database)
    _mb_product_getter: ProductGetter = Cake(ProductGetter, database=_database)
    _mb_matching_updater: MatchingUpdater = Cake(MatchingUpdater, database=_database)

    product_updater: ProductUpdatingService = Cake(
        ProductUpdatingService,
        stocks_getter=_yarvet_stocks_getter,
        price_getter=_yarvet_prices_getter,
        product_updater=_mb_product_updater,
        product_getter=_mb_product_getter,
    )
    matching_loader: LoadMatchingService = Cake(
        LoadMatchingService,
        matching_getter=_yarvet_product_getter,
        matching_updater=_mb_matching_updater,
    )
