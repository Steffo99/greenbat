import fastapi as f
import sqlalchemy.orm
import greenbat.database.engine
import greenbat.database.tables as tables
import greenbat.config
import greenbat.auth
import datetime


dep_user = greenbat.auth.Auth0User(domain=greenbat.config.cfg["authzero.domain"])


def dep_database():
    with greenbat.database.engine.Session(future=True) as session:
        yield session


def dep_dbuser(
        session: sqlalchemy.orm.Session = f.Depends(dep_database),
        claims: greenbat.auth.Auth0AccessClaims = f.Depends(dep_user),
):
    db_user = tables.User(
        sub=claims.sub,
        last_update=datetime.datetime.now(),
        name=claims.name,
        picture=claims.picture,
    )
    session.merge(db_user)
    return db_user
