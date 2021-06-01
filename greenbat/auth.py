import royalnet.royaltyping as t
import pydantic as p
import fastapi as f
import fastapi_cloudauth.auth0 as faca
import sqlalchemy.orm
import greenbat.database.engine
import greenbat.database.base
import greenbat.config
import datetime


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


def dep_dbuser(
        session: sqlalchemy.orm.Session = f.Depends(greenbat.database.engine.dep_database),
        claims: Auth0AccessClaims = f.Depends(Auth0User(domain=greenbat.config.cfg["authzero.domain"])),
):
    db_user = greenbat.database.base.User(
        sub=claims.sub,
        last_update=datetime.datetime.now(),
        name=claims.name,
        picture=claims.picture,
    )
    session.merge(db_user)
    return db_user
