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


router = f.APIRouter(
    tags=["Games"],
)


@router.get(
    "/all/",
    summary="List all games",
    response_model=list[models.get.GameGet]
)
def games_list(
        *,
        session: so.Session = f.Depends(deps.dep_session),
):
    return queries.list_(session, tables.Game)


@router.post(
    "/custom/",
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


@router.post(
    "/steam/",
    summary="Create a new Steam game",
    response_model=models.retrieve.GameRetrieve,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {
            "description": "Another game with the specified appid already exists",
            "model": models.retrieve.GameRetrieve,
        },
    },
    dependencies=[f.Depends(deps.dep_perms("create:game_steam"))]
)
def games_create_custom(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        metadata_steam: models.edit.MetadataSteamEdit = f.Body(...),
):
    if meta := session.execute(ss.select(tables.MetadataSteam).where(tables.MetadataSteam.appid) == metadata_steam.appid).one_or_none():
        raise f.HTTPException(status.HTTP_409_CONFLICT, meta.game)
    game = tables.Game()
    session.add(game)
    meta = tables.MetadataSteam(**metadata_steam.dict(), game=game)
    session.add(meta)
    session.commit()
    return game


@router.get(
    "/steam/{appid}",
    summary="Retrieve a Steam game by Steam appid",
    response_model=models.retrieve.GameRetrieve,
    responses={
        404: {
            "description": "No game with the specified Steam `appid` exists in the database",
        },
    },
)
def games_retrieve_steam(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        appid: int = f.Path(...),
):
    return queries.retrieve(session, tables.Game, tables.Game.metadata_steam.appid == appid)


@router.get(
    "/custom/mine/",
    summary="List all custom games created by the currently logged in user",
    response_model=list[models.get.GameGet],
)
def games_retrieve_steam(
        *,
        session: so.Session = f.Depends(deps.dep_session),
        user: tables.User = f.Depends(deps.dep_user),
):
    return queries.retrieve(session, tables.Game, tables.Game.metadata_custom.creator_sub == user.sub)


@router.get(
    "/all/{id}",
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
    "/custom/{id}",
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


@router.delete(
    "/all/{id}",
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
