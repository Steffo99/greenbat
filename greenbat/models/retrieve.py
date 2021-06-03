import greenbat.models._types as types
import greenbat.models._base as base
import greenbat.models.get as get


class ElementRetrieve(get.ElementGet):
    owner: get.UserGet
    game: get.GameGet


class MetadataSteamEdit(base.ORMModel):
    pass


class MetadataCustomEdit(base.ORMModel):
    pass


class GameRetrieve(get.GameGet):
    elements: list[get.ElementGet]


class AccountSteamRetrieve(get.AccountSteamGet):
    owner: get.UserGet


class UserRetrieve(get.UserGet):
    elements: list[get.ElementGet]
    accounts_steam: list[get.AccountSteamGet]
