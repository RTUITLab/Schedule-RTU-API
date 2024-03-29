import importlib
import time

from importlib import resources
from fastapi import FastAPI, Request, Response, Depends
from fastapi.middleware.cors import CORSMiddleware

from migrate import automigrate

from app.database.database import SessionLocal
from app.dependencies import get_settings, get_db


settings = get_settings()

app = FastAPI(
    title="Schedule-RTU API",
    version="5.0.0",
    dependencies=[Depends(get_db)],
    redoc_url=None,
    root_path=settings.root_path)

# include all routers
plugins = [f[:-3] for f in resources.contents("app.routers")
           if f.endswith(".py") and f[0] != "_"]
for plugin in plugins:
    if not "query" in plugin:
        router = importlib.import_module(f"app.routers.{plugin}")
        app.include_router(router.router)

# setup middleware

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
    start_time = time.time()
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# @app.on_event("startup")
# async def startup_event():
#     automigrate()
