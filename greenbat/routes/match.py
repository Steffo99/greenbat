from functools import reduce
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
from greenbat.config import cfg
from greenbat.utils.indoc import indoc


router = f.APIRouter()


@router.get(
    "/shared",
    summary="Get the list of games owned by all the specified users",
    description=indoc("""
        Retrieve the full array of games in common (**set intersection**) between all the specified users.
        
        _Useful to find out common interests, or what to play in multiplayer!_
    """),
    response_model=list[models.get.GameGet],
    responses={
        404: {
            "description": "User not found",
        },
    }
)
def _(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        subs: list[str] = f.Query(..., min_length=2, example=["auth0|5ed2debf7308300c1ea230c3", "auth0|5f3814421704af006de0c2e3"]),
):
    # FIXME: get users from subs!
    elements: t.Iterable[list[tables.Element]] = map(lambda sub: sub.elements, subs)
    games: t.Iterable[set[tables.Game]] = map(lambda elist: set(map(lambda e: e.game, elist)), elements)
    return reduce(lambda p, n: p.intersection(n), games)


@router.get(
    "/combined",
    summary="Get the list of games owned by at least one of the specified users",
    description=indoc("""
        Retrieve the full array of games owned by at least one (**set union**) of the specified users.
        
        _Useful to find out what games could be played having access to the libraries of the whole group!_ 
    """),
    response_model=list[models.get.GameGet],
    responses={
        404: {
            "description": "User not found",
        },
    }
)
def _(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        subs: list[str] = f.Query(..., min_length=2, example=["auth0|5ed2debf7308300c1ea230c3", "auth0|5f3814421704af006de0c2e3"]),
):
    # FIXME: get users from subs!
    elements: t.Iterable[list[tables.Element]] = map(lambda sub: sub.elements, subs)
    games: t.Iterable[set[tables.Game]] = map(lambda elist: set(map(lambda e: e.game, elist)), elements)
    return reduce(lambda p, n: p.union(n), games)
