import typing as t
import greenbat.models._types as types
import greenbat.models._base as base


class ElementEdit(base.ORMModel):
    pass


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
