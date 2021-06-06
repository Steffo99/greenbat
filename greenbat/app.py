import fastapi.middleware.cors
import pkg_resources
import greenbat.routes.users
import greenbat.routes.games_all
import greenbat.routes.games_custom
import greenbat.routes.games_steam
import greenbat.routes.elements


app = fastapi.FastAPI(
    debug=__debug__,
    title="Greenbat API",
    version=pkg_resources.get_distribution("greenbat").version,
    openapi_tags=[
        {
            "name": "Users",
            "description": "Operations with Greenbat users",
        },
        {
            "name": "Games (all)",
            "description": "Operations with games having any kind of metadata",
        },
        {
            "name": "Games (custom)",
            "description": "Operations with games having custom metadata",
        },
        {
            "name": "Games (Steam)",
            "description": "Operation with games having Steam metadata",
        },
        {
            "name": "Elements",
            "description": "Operations with library elements",
        }
    ],
)

app.include_router(greenbat.routes.users.router, prefix="/users", tags=["Users"])
app.include_router(greenbat.routes.games_all.router, prefix="/games/all", tags=["Games (all)"])
app.include_router(greenbat.routes.games_custom.router, prefix="/games/custom", tags=["Games (custom)"])
app.include_router(greenbat.routes.games_steam.router, prefix="/games/steam", tags=["Games (Steam)"])
app.include_router(greenbat.routes.elements.router, prefix="/elements", tags=["Elements"])
