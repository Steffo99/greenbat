import greenbat.models._types as types
import greenbat.models._base as base
import greenbat.models.get as get


class Element(get.Element):
    owner: get.User
    game: get.Game


class Game(get.Game):
    elements: list[get.Element]


class Steam(get.Steam):
    owner: get.User


class User(get.Steam):
    elements: list[get.Element]
    steams: list[get.Steam]
