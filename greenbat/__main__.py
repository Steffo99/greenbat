import uvicorn
import fastapi.middleware.cors
import greenbat.app
import greenbat.config


greenbat.app.app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=greenbat.config.cfg["api.alloworigins"],
    allow_methods=["*"],
    allow_headers=["*"],
)

uvicorn.run(greenbat.app.app, host="127.0.0.1", port=greenbat.config.cfg["api.port"])
