import uuid
import typing as t

import fastapi as f
import sqlalchemy.orm as so
import sqlalchemy.sql as ss
import starlette.status as status

import greenbat.models as models
import greenbat.dependencies as deps
import greenbat.database.tables as tables
import greenbat.utils.queries as queries
import greenbat.auth as auth


router = f.APIRouter()


@router.get(
    "/",
    summary="List all Steam games",
    response_model=list[models.get.GameGet],
)
def games_retrieve_steam(
        *,
        session: so.Session = f.Depends(deps.dep_session),
):
    return session.execute(
        ss.select(tables.Game).join(tables.MetadataSteam)
    ).fetchall()


@router.get(
    "/{appid}",
    summary="Retrieve a Steam game by Steam appid",
    response_model=models.retrieve.GameRetrieve,
    responses={
        404: {
            "description": "No game with the specified Steam `appid` exists in the database",
        },
    },
)
def games_retrieve_steam(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        appid: int = f.Path(...),
):
    return queries.retrieve(session, tables.Game, tables.Game.metadata_steam.appid == appid)


@router.post(
    "/",
    summary="Create a new Steam game",
    response_model=models.retrieve.GameRetrieve,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {
            "description": "Another game with the specified appid already exists",
            "model": models.retrieve.GameRetrieve,
        },
    },
    dependencies=[f.Depends(deps.dep_perms("create:game_steam"))]
)
def games_create_steam(
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
