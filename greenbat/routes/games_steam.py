import uuid
import typing as t

import fastapi as f
import sqlalchemy.exc
import sqlalchemy.orm as so
import sqlalchemy.sql as ss
import starlette.status as status

import greenbat.models as models
import greenbat.dependencies as deps
import greenbat.database.tables as tables
import greenbat.utils.queries as queries
import greenbat.auth as auth
from greenbat.config import cfg
from greenbat.utils.indoc import indoc


router = f.APIRouter()


@router.get(
    "/",
    summary="List all Steam games",
    description=indoc("""
        Get a paginated array listing all games with "steam" metadata registered on Greenbat.
        
        "Steam" games have an associated Steam store page, and can be identified by their Steam `appid`.
    """),
    response_model=list[models.get.GameGet],
)
def _(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        limit: int = f.Query(cfg["api.list.maxlimit"], le=cfg["api.list.maxlimit"]),
        offset: int = f.Query(0, ge=0),
):
    return queries.list_joined(session=session, tables=[tables.Game, tables.MetadataSteam], limit=limit, offset=offset)


@router.get(
    "/{appid}",
    summary="Retrieve a Steam game by Steam appid",
    description=indoc("""
        Get detailed information about the game with the specified Steam `appid`. 
    """),
    response_model=models.retrieve.GameRetrieve,
    responses={
        404: {
            "description": "No game with the specified Steam `appid` exists in the database",
        },
    },
)
def _(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        appid: int = f.Path(..., examples={
            "Dota 2": {
                "name": "Dota 2",
                "value": 570,
            },
            "Counter-Strike: Global Offensive": {
                "name": "Counter-Strike: Global Offensive",
                "value": 730,
            },
            "Baba is You": {
                "name": "Baba is You",
                "value": 736260,
            }
        }),
):
    try:
        return session.execute(
            ss.select(tables.Game).join(tables.MetadataSteam).where(tables.MetadataSteam.appid == appid)
        ).scalar()
    except sqlalchemy.exc.NoResultFound:
        raise f.HTTPException(404, "No game with the specified Steam `appid` exists in the database")


@router.post(
    "/",
    summary="Create a new Steam game",
    description=indoc("""
        Manually create a single Steam game.
    """),
    response_model=models.retrieve.GameRetrieve,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {
            "description": "Another game with the specified appid already exists",
            "model": models.retrieve.GameRetrieve,
        },
    },
)
def _(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        metadata_steam: models.edit.MetadataSteamEdit = f.Body(...),
):
    if meta := session.execute(ss.select(tables.MetadataSteam).where(tables.MetadataSteam.appid) == metadata_steam.appid).one_or_none():
        raise f.HTTPException(status.HTTP_409_CONFLICT, meta.game)

    game = tables.Game()
    session.add(game)
    meta = tables.MetadataSteam(**metadata_steam.dict(), game=game)
    session.add(meta)
    session.commit()
    return game
