import pydantic
import datetime
import greenbat.models._types as types
import greenbat.models._base as base


class Element(base.Model):
    uuid: pydantic.UUID4
    owner_id: str
    game_id: pydantic.UUID4


class Game(base.Model):
    uuid: pydantic.UUID4
    name: str


class Steam(base.Model):
    steamid: types.SteamID
    owner_id: str


class User(base.Model):
    sub: str
    last_update: datetime.datetime
    name: str
    picture: pydantic.HttpUrl
