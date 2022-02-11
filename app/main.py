import importlib

from importlib import resources
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from migrate import automigrate

from app.database.database import SessionLocal
from app.dependencies import get_settings


settings = get_settings()

app = FastAPI(root_path=settings.root_path)

# include all routers
plugins = [f[:-3] for f in resources.contents("app.routers")
           if f.endswith(".py") and f[0] != "_"]
for plugin in plugins:
    router = importlib.import_module(f"app.routers.{plugin}")
    app.include_router(router.router)

# setup middleware
if settings.debug:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


@app.on_event("startup")
async def startup_event():
    automigrate()
