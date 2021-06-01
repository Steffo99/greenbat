import pydantic
import steam.steamid


class SteamID(steam.steamid.SteamID):
    @classmethod
    def __get_validators__(cls):
        yield lambda v: cls(v)

    @classmethod
    def __modify_schema__(cls, field_schema: pydantic):
        field_schema.update(
            examples=[
                12345,
                '12345',
                103582791429521412,
                '103582791429521412',
                'STEAM_1:0:2',
                '[g:1:4]'
            ]
        )
