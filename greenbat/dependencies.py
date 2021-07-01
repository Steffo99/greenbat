import fastapi as f
import fastapi.security as fs
import starlette.status as s
import sqlalchemy.orm
import greenbat.database.engine
import greenbat.database.tables as tables
import greenbat.config
import greenbat.auth as auth
import datetime
import jose.jwt


def dep_session():
    with greenbat.database.engine.Session(future=True) as session:
        yield session


def dep_claims(
        token: str = f.Depends(auth.scheme)
) -> auth.RYGLoginClaims:
    try:
        unverified = jose.jwt.get_unverified_headers(token)
    except jose.jwt.JWTError as e:
        raise f.HTTPException(f.status.HTTP_401_UNAUTHORIZED, f"JWT: {e.args[0]}")

    try:
        payload = jose.jwt.decode(token, auth.jwks[unverified["kid"]], audience=auth.audience, algorithms=["RS256"])
    except KeyError:
        raise f.HTTPException(f.status.HTTP_401_UNAUTHORIZED, "JWT: Unknown kid")
    except jose.jwt.JWTError as e:
        raise f.HTTPException(f.status.HTTP_401_UNAUTHORIZED, f"JWT: {e.args[0]}")

    return auth.RYGLoginClaims(**payload)


def dep_user(
        session: sqlalchemy.orm.Session = f.Depends(dep_session),
        claims: auth.RYGLoginClaims = f.Depends(dep_claims),
):
    db_user = tables.User(
        sub=claims.sub,
        last_update=datetime.datetime.now(),
        name=claims.name,
        picture=claims.picture,
    )
    db_user = session.merge(db_user)
    session.commit()
    return db_user


def dep_perms(*perms: str):
    def actual_dep(claims: auth.RYGLoginClaims = f.Depends(dep_claims)):
        if not claims.has_permissions(*perms):
            raise f.HTTPException(s.HTTP_403_FORBIDDEN, "Insufficient permissions or scope.")
    return actual_dep
