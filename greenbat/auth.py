import royalnet.royaltyping as t
import pydantic as p
import fastapi_cloudauth.auth0 as faca


class Auth0AccessClaims(p.BaseModel):
    iss: str
    sub: str
    aud: t.Union[t.List[str], str]
    iat: int
    exp: int
    azp: str
    scope: str
    permissions: t.List[str] = p.Field([])
    name: str = p.Field(..., alias="https://meta.ryg.one/name")
    picture: p.HttpUrl = p.Field(..., alias="https://meta.ryg.one/picture")


class Auth0User(faca.Auth0CurrentUser):
    user_info = Auth0AccessClaims
