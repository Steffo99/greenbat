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
from greenbat.config import cfg
from greenbat.utils.indoc import indoc


router = f.APIRouter()


@router.get(
    "/",
    summary="List all custom games",
    description=indoc("""
        Get a paginated array listing all games with "custom" metadata registered on Greenbat.
    """),
    response_model=list[models.get.GameGet],
)
def _(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        limit: int = f.Query(cfg["api.list.maxlimit"], le=cfg["api.list.maxlimit"]),
        offset: int = f.Query(0, ge=0),
):
    return queries.list_joined(session=session, tables=[tables.Game, tables.MetadataCustom], limit=limit, offset=offset)


@router.get(
    "/mine/",
    summary="List all custom games created by the currently logged in user",
    description=indoc("""
        Get a paginated array listing all games with "custom" metadata created by the currently logged in user.
    """),
    response_model=list[models.get.GameGet],
)
def _(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        user: tables.User = f.Depends(deps.dep_user),
        limit: int = f.Query(cfg["api.list.maxlimit"], le=cfg["api.list.maxlimit"]),
        offset: int = f.Query(0, ge=0),
):
    return session.execute(
        ss.select(tables.Game).join(tables.MetadataCustom).where(tables.MetadataCustom.creator == user).limit(limit).offset(offset)
    ).all()


@router.post(
    "/mine/",
    summary="Create a new custom game",
    description=indoc("""
        Create a new game with "custom" metadata, and set the currently logged in user as its owner.
    """),
    response_model=models.retrieve.GameRetrieve,
    status_code=status.HTTP_201_CREATED,
)
def _(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        user: tables.User = f.Depends(deps.dep_user),
        metadata_custom: models.edit.MetadataCustomEdit = f.Body(...),
):
    game = tables.Game()
    session.add(game)
    meta = tables.MetadataCustom(**metadata_custom.dict(), creator=user, game=game)
    session.add(meta)
    session.commit()
    return game


@router.delete(
    "/mine/{id}",
    summary="Delete a custom game created by the currently logged in user",
    description=indoc("""
        Permanently delete the game with the specified `id`, all its metadata **AND all elements attached to it**, 
        but only if the currently logged in user is its owner.
    """),
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=f.Response,
    responses={
        403: {
            "description": "User is not the creator of the custom game",
            "model": models.retrieve.GameRetrieve,
        },
        404: {
            "description": "No game with the specified Greenbat `id` exists in the database",
        },
        405: {
            "description": "Game is not custom",
            "model": models.retrieve.GameRetrieve,
        }
    },
)
def _(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        user: tables.User = f.Depends(deps.dep_user),
        id: int = f.Path(..., example=1),
):
    game = queries.retrieve(session, tables.Game, tables.Game.id == id)

    if not game.metadata_custom:
        raise f.HTTPException(405, game)

    if not game.metadata_custom.creator == user:
        raise f.HTTPException(403, game)

    session.delete(game)
    session.commit()


@router.get(
    "/of/{sub}/",
    summary="List all custom games created by the specified user",
    description=indoc("""
        Get a paginated array listing all games with "custom" metadata created by the currently logged in user.
    """),
    response_model=list[models.get.GameGet],
)
def _(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        sub: str = f.Path(...),
        limit: int = f.Query(cfg["api.list.maxlimit"], le=cfg["api.list.maxlimit"]),
        offset: int = f.Query(0, ge=0),
):
    return session.execute(
        ss.select(tables.Game).join(tables.MetadataCustom).where(tables.MetadataCustom.creator_sub == sub).limit(limit).offset(offset)
    ).fetchall()
