import fastapi as f
import sqlalchemy.orm as so

import greenbat.models as models
import greenbat.dependencies as deps
import greenbat.database.tables as tables
import greenbat.utils.queries as queries
from greenbat.config import cfg


router = f.APIRouter()


@router.get(
    "/",
    summary="List all the registered users",
    response_model=list[models.get.UserGet],
)
def _(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        limit: int = f.Query(cfg["api.list.maxlimit"], le=cfg["api.list.maxlimit"]),
        offset: int = f.Query(0, ge=0),
):
    return queries.list_(session=session, table=tables.User, limit=limit, offset=offset)


@router.get(
    "/me",
    summary="Retrieve details about the currently logged in user",
    response_model=models.retrieve.UserRetrieve,
)
def _(
        *,
        user: tables.User = f.Depends(deps.dep_user),
):
    return user


@router.get(
    "/{sub}",
    summary="Retrieve details about a single registered user",
    response_model=models.retrieve.UserRetrieve,
    responses={
        404: {},
    }
)
def _(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        sub: str = f.Path(...),
):
    return queries.retrieve(session=session, table=tables.User, condition=tables.User.sub == sub)
