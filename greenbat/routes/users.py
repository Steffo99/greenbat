import fastapi as f
import sqlalchemy.orm as so

import greenbat.models as models
import greenbat.dependencies as deps
import greenbat.database.tables as tables
import greenbat.utils.queries as queries


router = f.APIRouter(
    tags=["Users"],
)


@router.get(
    "/",
    summary="List all the registered users.",
    response_model=list[models.get.UserGet],
)
def users_list(
        *,
        session: so.Session = f.Depends(deps.dep_session),
):
    return queries.list_(session, tables.User)


@router.get(
    "/me",
    summary="Retrieve details about the currently logged in user.",
    response_model=models.retrieve.UserRetrieve,
)
def users_retrieve_me(
        *,
        user: tables.User = f.Depends(deps.dep_user),
):
    return user


@router.get(
    "/{sub}",
    summary="Retrieve details about a single registered user.",
    response_model=models.retrieve.UserRetrieve,
    responses={
        404: {"message": "Not found"},
    }
)
def users_retrieve(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        sub: str = f.Path(...),
):
    return queries.retrieve(session, tables.User, tables.User.sub == sub)