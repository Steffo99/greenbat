import typing as t
import pydantic
import datetime
import greenbat.models._types as types
import greenbat.models._base as base
import greenbat.models.edit as edit


class ElementGet(edit.ElementEdit):
    id: int
    owner_id: str


class MetadataSteamGet(edit.MetadataSteamEdit):
    pass


class MetadataCustomGet(edit.MetadataCustomEdit):
    pass


class GameGet(edit.GameEdit):
    id: int
    metadata_steam: t.Optional[MetadataSteamGet]
    metadata_custom: t.Optional[MetadataCustomGet]


class AccountSteamGet(edit.AccountSteamEdit):
    steamid: types.SteamID
    owner_id: str


class UserGet(edit.UserEdit):
    sub: str
    last_update: datetime.datetime
    name: str
    picture: pydantic.HttpUrl
