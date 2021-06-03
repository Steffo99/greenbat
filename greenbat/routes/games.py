import uuid

import fastapi as f
import sqlalchemy.orm as so
import starlette.status as status

import greenbat.models as models
import greenbat.dependencies as deps
import greenbat.database.tables as tables
import greenbat.utils.queries as queries
import greenbat.auth as auth


router = f.APIRouter(
    tags=["Games"],
)


@router.get("/", summary="List all logged games.", response_model=list[models.get.GameGet])
def games_list(
        *,
        session: so.Session = f.Depends(deps.dep_session),
):
    return queries.list_(session, tables.Game)


@router.post("/", summary="Create a new custom game.", response_model=models.retrieve.GameRetrieve, status_code=status.HTTP_201_CREATED)
def games_create(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        claims: auth.Auth0AccessClaims = f.Depends(deps.dep_claims),
        user: tables.User = f.Depends(deps.dep_user),
        metadata_custom: models.edit.MetadataCustomEdit = f.Body(...),
):
    game = tables.Game()
    session.add(game)
    meta = tables.MetadataCustom(**metadata_custom.dict(), game=game)
    session.add(meta)
    session.commit()
    return game


@router.get("/{gid}", summary="Retrieve a specific logged game by UUID.", response_model=models.retrieve.GameRetrieve)
def games_retrieve(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        gid: uuid.UUID = f.Path(...),
):
    return queries.retrieve(session, tables.Game, tables.Game.uuid == gid)


@router.delete("/{gid}", summary="Delete a logged game.", status_code=status.HTTP_204_NO_CONTENT, response_class=f.Response)
def games_destroy(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        claims: auth.Auth0AccessClaims = f.Depends(deps.dep_claims),
        user: tables.User = f.Depends(deps.dep_user),
        gid: uuid.UUID = f.Path(...),
):
    return queries.destroy(session, tables.Game, tables.Game.uuid == gid)
