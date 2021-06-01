import fastapi
import fastapi.middleware.cors
import pkg_resources
import greenbat.routes.example


app = fastapi.FastAPI(
    debug=__debug__,
    title="Greenbat API",
    version=pkg_resources.get_distribution("greenbat").version,
)

app.include_router(greenbat.routes.example.router, prefix="/example")
