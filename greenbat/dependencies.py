import fastapi as f
import fastapi.security as fs
import starlette.status as s
import sqlalchemy.orm
import greenbat.database.engine
import greenbat.database.tables as tables
import greenbat.config
import greenbat.auth
import datetime


def dep_session():
    with greenbat.database.engine.Session(future=True) as session:
        yield session


def dep_user(
        session: sqlalchemy.orm.Session = f.Depends(dep_session),
        claims: greenbat.auth.RYGLoginClaims = f.Depends(greenbat.auth.dep_claims),
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
    def actual_dep(claims: greenbat.auth.RYGLoginClaims = f.Depends(greenbat.auth.dep_claims)):
        if not claims.has_permissions(*perms):
            raise f.HTTPException(s.HTTP_403_FORBIDDEN, "Insufficient permissions or scope.")
    return actual_dep
