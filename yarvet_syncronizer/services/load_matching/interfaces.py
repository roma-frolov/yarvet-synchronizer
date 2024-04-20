import typing


class IMatching(typing.Protocol):
    id: int
    article_number: str


class IMatchingUpdater(typing.Protocol):
    async def batch_update(self, matchings: typing.Sequence[IMatching]) -> None: ...


class IMatchingGetter(typing.Protocol):
    async def get_matchings_of_ids_to_articles(self) -> typing.Sequence[IMatching]: ...
