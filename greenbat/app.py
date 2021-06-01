import fastapi
import pkg_resources

app = fastapi.FastAPI(
    debug=__debug__,
    title="Green Bat API",
    version=pkg_resources.get_distribution("greenbat").version,
)
