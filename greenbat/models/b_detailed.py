import greenbat.models._types as types
import greenbat.models._base as base
import greenbat.models.a_basic as basic


class Element(basic.Element):
    owner: basic.User
    game: basic.Game


class Game(basic.Game):
    elements: list[basic.Element]


class Steam(basic.Steam):
    owner: basic.User


class User(basic.Steam):
    elements: list[basic.Element]
    steams: list[basic.Steam]
