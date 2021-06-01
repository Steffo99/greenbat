import fastapi as f
import greenbat.database.engine
import greenbat.auth


router = f.APIRouter()


@router.get("/")
def example(
        session = f.Depends(greenbat.database.engine.dep_database),
        user = f.Depends(greenbat.auth.dep_dbuser),
):
    breakpoint()
