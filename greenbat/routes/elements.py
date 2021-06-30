import uuid
import typing as t

import fastapi as f
import sqlalchemy.orm as so
import sqlalchemy.sql as ss
import starlette.status as status

import greenbat.models as models
import greenbat.dependencies as deps
import greenbat.database.tables as tables
import greenbat.database.enums as enums
import greenbat.utils.queries as queries
import greenbat.auth as auth
from greenbat.utils.indoc import indoc
from greenbat.config import cfg


router = f.APIRouter()


@router.get(
    "/",
    summary="List all elements in the database",
    description=indoc("""
        Get a paginated array of all the elements contained in the database.
    """),
    response_model=list[models.get.ElementGet],
)
def _(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        limit: int = f.Query(cfg["api.list.maxlimit"], le=cfg["api.list.maxlimit"]),
        offset: int = f.Query(0, ge=0),
):
    return queries.list_(session=session, table=tables.Element, limit=limit, offset=offset)


@router.get(
    "/{id}",
    summary="Retrieve an element",
    description=indoc("""
        Get detailed information about the element with the specified `id`. 
    """),
    response_model=models.retrieve.ElementRetrieve,
    responses={
        404: {
            "description": "No element with the specified `id` exists in the database",
        },
    },
)
def _(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        id: int = f.Path(..., example=1),
):
    return queries.retrieve(session, tables.Element, tables.Element.id == id)


@router.delete(
    "/{id}",
    summary="Delete an element",
    description=indoc("""
        Permanently delete the element with the specified `id`.
    """),
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=f.Response,
    responses={
        404: {
            "description": "No element with the specified `id` exists in the database",
        },
    },
)
def _(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        id: int = f.Path(..., example=1),
):
    return queries.destroy(session, tables.Element, tables.Element.id == id)


@router.get(
    "/mine/",
    summary="List all elements in the library of the currently logged in user",
    description=indoc("""
        Get a paginated array listing all the elements having the currently logged in user as owner. 
    """),
    response_model=list[models.get.ElementGet],
)
def _(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        user: tables.User = f.Depends(deps.dep_user),
        limit: int = f.Query(cfg["api.list.maxlimit"], le=cfg["api.list.maxlimit"]),
        offset: int = f.Query(0, ge=0),
):
    return queries.list_(session=session, table=tables.Element, condition=tables.Element.owner == user, limit=limit, offset=offset)


@router.get(
    "/of/{sub}/",
    summary="List all elements in the library of the specified user",
    description=indoc("""
        Get a paginated array listing all the elements having the specified `sub` as owner. 
    """),
    response_model=list[models.get.ElementGet],
)
def _(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        sub: str = f.Path(..., example="auth0|5ed2debf7308300c1ea230c3"),
        limit: int = f.Query(cfg["api.list.maxlimit"], le=cfg["api.list.maxlimit"]),
        offset: int = f.Query(0, ge=0),
):
    return queries.list_(session=session, table=tables.Element, condition=tables.Element.owner_id == sub, limit=limit, offset=offset)


@router.post(
    "/mine/",
    summary="Add a new element to the library of the currently logged in user",
    description=indoc("""
        Create a new element with the passed `data` having the currently logged in user as owner.
        
        Obviously, _users cannot create elements for users other than themselves_!
    """),
    status_code=status.HTTP_201_CREATED,
    response_model=models.retrieve.ElementRetrieve,
)
def _(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        user: tables.User = f.Depends(deps.dep_user),
        data: models.edit.ElementEdit = f.Body(...),
):
    return queries.create(session=session, table=tables.Element, model_data=data, owner=user)


@router.put(
    "/mine/{id}",
    summary="Edit an element owned by the currently logged in user",
    description=indoc("""
        Edit the element with the passed `id` with `data`, but only if the owner is the currently logged in user.
    """),
    status_code=status.HTTP_200_OK,
    response_model=models.retrieve.ElementRetrieve,
    responses={
        404: {
            "description": "No element with the specified `id` is owned by the user",
        },
    },
)
def _(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        user: tables.User = f.Depends(deps.dep_user),
        id: int = f.Path(..., example=1),
        data: models.edit.ElementEdit = f.Body(...),
):
    return queries.edit(session, tables.Element, ss.and_(tables.Element.id == id, tables.Element.owner == user), data)


@router.delete(
    "/mine/{id}",
    summary="Delete an element owned by the currently logged in user",
    description=indoc("""
        Permanently delete the element with the passed `id`, but only if its owner is the currently logged in user.
    """),
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=f.Response,
    responses={
        404: {
            "description": "No element with the specified `id` is owned by the user",
        },
    },
)
def _(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        user: tables.User = f.Depends(deps.dep_user),
        id: int = f.Path(..., example=1),
):
    queries.destroy(session, tables.Element, ss.and_(tables.Element.id == id, tables.Element.owner == user))


@router.patch(
    "/mine/{id}/rating",
    summary="Rate an element owned by the currently logged in user.",
    description=indoc("""
        Quickly set the `rating` of the element with the passed `id`, but only if its owner is the currently logged in user.
    """),
    status_code=status.HTTP_200_OK,
    response_model=models.retrieve.ElementRetrieve,
    responses={
        404: {
            "description": "No element with the specified `id` is owned by the user",
        },
    },
)
def _(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        user: tables.User = f.Depends(deps.dep_user),
        id: int = f.Path(..., example=1),
        rating: enums.Rating = f.Body(..., example=enums.Rating.LIKED)
):
    element = queries.retrieve(session, tables.Element, ss.and_(tables.Element.id == id, tables.Element.owner == user))
    element.rating = rating
    session.commit()
    return element


@router.patch(
    "/mine/{id}/completition",
    summary="Change completition for an element owned by the currently logged in user.",
    description=indoc("""
        Quickly set the `completition` of the element with the passed `id`, but only if its owner is the currently logged in user.
    """),
    status_code=status.HTTP_200_OK,
    response_model=models.retrieve.ElementRetrieve,
    responses={
        404: {
            "description": "No element with the specified `id` is owned by the user",
        },
    },
)
def _(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        user: tables.User = f.Depends(deps.dep_user),
        id: int = f.Path(..., example=1),
        completition: enums.Completition = f.Body(..., example=enums.Completition.COMPLETED)
):
    element = queries.retrieve(session, tables.Element, ss.and_(tables.Element.id == id, tables.Element.owner == user))
    element.completition = completition
    session.commit()
    return element
