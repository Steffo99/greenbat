import typing as t
import greenbat.models._types as types
import greenbat.database.enums as enums
import greenbat.models._base as base


class ElementEdit(base.ORMModel):
    rating: t.Optional[enums.Rating]
    completition: t.Optional[enums.Completition]
    game_id: int


class MetadataSteamEdit(base.ORMModel):
    appid: int
    title: str


class MetadataCustomEdit(base.ORMModel):
    title: str
    url: str


class GameEdit(base.ORMModel):
    pass


class AccountSteamEdit(base.ORMModel):
    pass


class UserEdit(base.ORMModel):
    pass
