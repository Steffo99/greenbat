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
    summary="List all custom games",
    response_model=list[models.get.GameGet],
)
def games_retrieve_steam(
        *,
        session: so.Session = f.Depends(deps.dep_session),
):
    return session.execute(
        ss.select(tables.Game).join(tables.MetadataCustom)
    ).fetchall()


@router.post(
    "/",
    summary="Create a new custom game",
    response_model=models.retrieve.GameRetrieve,
    status_code=status.HTTP_201_CREATED,
    dependencies=[f.Depends(deps.dep_perms("create:game_custom"))]
)
def games_create_custom(
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


@router.get(
    "/mine/",
    summary="List all custom games created by the currently logged in user",
    response_model=list[models.get.GameGet],
)
def games_retrieve_steam(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        user: tables.User = f.Depends(deps.dep_user),
):
    return queries.retrieve(session, tables.Game, tables.Game.metadata_custom.creator_sub == user.sub)


@router.delete(
    "/mine/{id}",
    summary="Delete a custom game you created yourself",
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
    dependencies=[f.Depends(deps.dep_perms("destroy:game_custom"))],
)
def games_destroy_custom(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        user: tables.User = f.Depends(deps.dep_user),
        id: int = f.Path(...),
):
    game = queries.retrieve(session, tables.Game, tables.Game.uuid == id)

    if not game.metadata_custom:
        raise f.HTTPException(405, game)

    if not game.creator == user:
        raise f.HTTPException(403, game)

    session.delete(game)
    session.commit()
