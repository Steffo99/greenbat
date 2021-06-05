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
    summary="List all games",
    response_model=list[models.get.GameGet]
)
def games_list(
        *,
        session: so.Session = f.Depends(deps.dep_session),
):
    return queries.list_(session, tables.Game)


@router.get(
    "/{id}",
    summary="Retrieve a game by Greenbat id",
    response_model=models.retrieve.GameRetrieve,
    responses={
        404: {
            "description": "No game with the specified Greenbat `id` exists in the database",
        },
    },
)
def games_retrieve_all(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        id: int = f.Path(...),
):
    return queries.retrieve(session, tables.Game, tables.Game.uuid == id)


@router.delete(
    "/{id}",
    summary="Delete a game",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=f.Response,
    responses={
        404: {
            "description": "No game with the specified Greenbat `id` exists in the database",
        },
    },
    dependencies=[f.Depends(deps.dep_perms("destroy:game_all"))],
)
def games_destroy_custom(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        id: int = f.Path(...),
):
    queries.destroy(session, tables.Game, tables.Game.uuid == id)
