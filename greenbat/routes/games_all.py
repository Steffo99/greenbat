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
    summary="List all games",
    description=indoc("""
        Get a paginated array listing all games registered on Greenbat, providing their metadata where possible.
    """),
    response_model=list[models.get.GameGet],
)
def _(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        limit: int = f.Query(cfg["api.list.maxlimit"], le=cfg["api.list.maxlimit"]),
        offset: int = f.Query(0, ge=0),
):
    return queries.list_(session=session, table=tables.Game, limit=limit, offset=offset)


@router.get(
    "/{id}",
    summary="Retrieve a game by Greenbat id",
    description=indoc("""
        Get detailed information about the game with the specified `id`. 
    """),
    response_model=models.retrieve.GameRetrieve,
    responses={
        404: {
            "description": "No game with the specified Greenbat `id` exists in the database",
        },
    },
)
def _(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        id: int = f.Path(..., example=1),
):
    return queries.retrieve(session=session, table=tables.Game, condition=tables.Game.uuid == id)


@router.delete(
    "/{id}",
    summary="Delete a game",
    description=indoc("""
        Permanently delete the game with the specified `id`, all its metadata **AND all elements attached to it**. 
    """),
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=f.Response,
    responses={
        404: {
            "description": "No game with the specified Greenbat `id` exists in the database",
        },
    },
)
def _(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        id: int = f.Path(..., example=1),
):
    queries.destroy(session=session, table=tables.Game, condition=tables.Game.uuid == id)
