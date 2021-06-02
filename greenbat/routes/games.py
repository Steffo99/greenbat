import uuid

import fastapi as f
import sqlalchemy.orm as so
import starlette.status as status

import greenbat.models as models
import greenbat.dependencies as deps
import greenbat.database.tables as tables
import greenbat.utils.queries as queries


router = f.APIRouter(
    tags=["Games"],
)


@router.get("/", summary="List all logged games.", response_model=list[models.get.Game])
def games_list(
        *,
        session: so.Session = f.Depends(deps.dep_database),
):
    return queries.list_(session, tables.Game)


@router.post("/", summary="Log a new game.", response_model=models.retrieve.Game, status_code=status.HTTP_201_CREATED)
def games_create(
        *,
        session: so.Session = f.Depends(deps.dep_database),
        user: tables.User = f.Depends(deps.dep_dbuser),
        game: models.edit.Game = f.Body(...),
):
    return queries.create(session, tables.Game, game)


@router.get("/{gid}", summary="Retrieve a specific logged game by UUID.", response_model=models.retrieve.Game)
def games_retrieve(
        *,
        session: so.Session = f.Depends(deps.dep_database),
        gid: uuid.UUID = f.Path(...),
):
    return queries.retrieve(session, tables.Game, tables.Game.uuid == gid)


@router.put("/{gid}", summary="Edit a logged game's details.", response_model=models.retrieve.Game)
def games_edit(
        *,
        session: so.Session = f.Depends(deps.dep_database),
        user: tables.User = f.Depends(deps.dep_dbuser),
        gid: uuid.UUID = f.Path(...),
        game: models.edit.Game = f.Body(...),
):
    return queries.edit(session, tables.Game, tables.Game.uuid == gid, game)


@router.delete("/{gid}", summary="Delete a logged game.", status_code=status.HTTP_204_NO_CONTENT, response_class=f.Response)
def games_destroy(
        *,
        session: so.Session = f.Depends(deps.dep_database),
        user: tables.User = f.Depends(deps.dep_dbuser),
        gid: uuid.UUID = f.Path(...),
):
    return queries.destroy(session, tables.Game, tables.Game.uuid == gid)
