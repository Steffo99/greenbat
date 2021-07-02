import royalnet.royaltyping as t
import pydantic as p
import fastapi.security as fs
import requests

from greenbat.config import cfg


jwks = requests.get(cfg["auth.jwks"]).json()
jwks = {jwk["kid"]: jwk for jwk in jwks.get("keys", [])}


audience = cfg["auth.audience"]


scheme = fs.OAuth2AuthorizationCodeBearer(
    authorizationUrl=cfg["auth.authorization"],
    tokenUrl=cfg["auth.token"],
    refreshUrl=cfg["auth.refresh"],
    scopes={
        "openid": "[Required] Login using OpenID connect",
        "email": "[Required] Get the logged user's email",
        "profile": "[Required] Get information about the logged user",

        "create:element": "Create new elements on the user's behalf",
        "rate:element": "Rate elements on the user's behalf",
        "complete:element": "Complete elements on the user's behalf",
        "destroy:element": "Delete the user's elements",

        "edit:any_game": "[Admin] Edit game metadata",
        "destroy:any_game": "[Admin] Delete games",

        "create:game_custom": "Create new games with custom metadata on the user's behalf",
        "edit:game_custom": "Edit the games with custom metadata created by the user",
        "destroy:game_custom": "Delete the games with custom metadata created by the user",

        "create:game_steam": "[Admin] Manually create new games with steam metadata",

        "sync:library_steam": "Syncronize the user's Steam library to Greenbat"
    }
)


class RYGLoginClaims(p.BaseModel):
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

    def has_permissions(self, *perms):
        for perm in perms:
            if perm not in self.permissions:
                return False
        else:
            return True
