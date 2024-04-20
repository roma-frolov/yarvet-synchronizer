import typing

from yarvet_syncronizer.services.load_matching.interfaces import IMatching, IMatchingGetter, IMatchingUpdater


class LoadMatchingService:
    def __init__(
        self,
        matching_getter: IMatchingGetter,
        matching_updater: IMatchingUpdater,
    ) -> None:
        self.matching_getter: typing.Final[IMatchingGetter] = matching_getter
        self.matching_updater: typing.Final[IMatchingUpdater] = matching_updater

    async def load_matchings(self) -> None:
        matchings: typing.Sequence[IMatching] = await self.matching_getter.get_matchings_of_ids_to_articles()
        await self.matching_updater.batch_update(matchings)
