import royalnet.royaltyping as t
import pydantic as p
import fastapi as f
import fastapi.security as fs
import fastapi.openapi.models as fom
import fastapi_cloudauth as fc
import jose
import jose.jwt

from greenbat.config import cfg


scheme = fs.OAuth2AuthorizationCodeBearer(
    authorizationUrl=cfg["auth.authorization"],
    tokenUrl=cfg["auth.token"],
    refreshUrl=cfg["auth.refresh"],
    scopes={
        "openid": "[Required] Login using OpenID connect",
        "email": "[Required] Get the logged user's email",
        "profile": "[Required] Get information about the logged user",

        "create:element": "Create new elements on the user's behalf",
        "edit:element": "Change the status of the user's elements",
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


def dep_claims(
        token: str = f.Depends(scheme)
) -> RYGLoginClaims:
    try:
        payload = jose.jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user