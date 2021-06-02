import pydantic
import datetime
import greenbat.models._types as types
import greenbat.models._base as base
import greenbat.models.edit as edit


class Element(edit.Element):
    uuid: pydantic.UUID4
    owner_id: str
    game_id: pydantic.UUID4


class Game(edit.Game):
    uuid: pydantic.UUID4
    name: str


class Steam(edit.Steam):
    steamid: types.SteamID
    owner_id: str


class User(edit.User):
    sub: str
    last_update: datetime.datetime
    name: str
    picture: pydantic.HttpUrl
