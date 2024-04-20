import asyncio
import contextlib

import aiocron
from loguru import logger

from yarvet_syncronizer.container import Container


@aiocron.crontab("* * * * *")
async def update_products() -> None:
    logger.debug("Updated products started")

    if not Container.__bakery_visitors__:
        await Container.aopen()

    await Container.product_updater().update_products()  # type: ignore[operator]
    logger.debug("Updated products completed")


@aiocron.crontab("*/30 * * * *")
async def load_matchings() -> None:
    logger.debug("Load matchings started")

    if not Container.__bakery_visitors__:
        await Container.aopen()

    await Container.matching_loader().load_matchings()  # type: ignore[operator]
    logger.debug("Load matchings completed")


async def shutdown() -> None:
    await Container.aclose()


async def main() -> None:
    async with Container() as container:
        await container.matching_loader.load_matchings()


if __name__ == "__main__":
    logger.debug("Application startup")
    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

    with contextlib.suppress(KeyboardInterrupt):
        loop.run_forever()

    loop.run_until_complete(shutdown())
    logger.debug("Application shutdown")
