import sqlalchemy.types
import steam.steamid


class SteamID(sqlalchemy.types.TypeDecorator):
    """
    Converts values from and to :class:`steam.steamid.SteamID`\\ s.
    """

    impl = sqlalchemy.types.BigInteger
    cache_ok = True

    def process_bind_param(self, value: steam.steamid.SteamID, dialect):
        return value.as_64

    def process_literal_param(self, value: steam.steamid.SteamID, dialect):
        return value.as_64

    def process_result_value(self, value: int, dialect):
        return steam.steamid.SteamID(value)

    @property
    def python_type(self):
        return steam.steamid.SteamID
