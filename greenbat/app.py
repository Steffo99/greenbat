import pathlib
import fastapi.middleware.cors
import pkg_resources
import greenbat.routes.users
import greenbat.routes.games_all
import greenbat.routes.games_custom
import greenbat.routes.games_steam
import greenbat.routes.elements
import greenbat.routes.match


this_path = pathlib.Path(__file__)
dist_path = this_path.parent
desc_path = dist_path.joinpath("description.md")
with open(desc_path) as file:
    description = file.read()


app = fastapi.FastAPI(
    debug=__debug__,
    title="Greenbat API",
    description=description,
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
            "description": "Operations with games having Steam metadata",
        },
        {
            "name": "Elements",
            "description": "Operations with library elements",
        },
        {
            "name": "Match",
            "description": "Comparisions between users' libraries"
        }
    ],
)

app.include_router(greenbat.routes.users.router, prefix="/users", tags=["Users"])
app.include_router(greenbat.routes.games_all.router, prefix="/games/all", tags=["Games (all)"])
app.include_router(greenbat.routes.games_custom.router, prefix="/games/custom", tags=["Games (custom)"])
app.include_router(greenbat.routes.games_steam.router, prefix="/games/steam", tags=["Games (Steam)"])
app.include_router(greenbat.routes.elements.router, prefix="/elements", tags=["Elements"])
app.include_router(greenbat.routes.match.router, prefix="/match", tags=["Match"])
