import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy_utils import drop_database, database_exists, create_database
from starlette.middleware import Middleware
from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware
from starlette_context.plugins.base import Plugin
from middlewares import (
    LogRequestMiddleware,
    RequestPlugin,
)
from model import Base, get_db, engine, User
import config
import src


class AuthorizationPlugin(Plugin):
    """
    Customize plugin to get jwt token
    """

    key = "Authorization"


middleware = [
    Middleware(
        RawContextMiddleware,
        plugins=(plugins.RequestIdPlugin(), RequestPlugin()),
    ),
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    Middleware(LogRequestMiddleware),
]

app = FastAPI(middleware=middleware)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router
app.include_router(src.routes)


def initialize(db_uri: str) -> None:
    # Create database
    if database_exists(db_uri):
        return
    create_database(db_uri)
    Base.metadata.create_all(engine)

    # depend
    db = next(get_db())
    default_user = User(
        email=config.get("ADMIN_INIT_EMAIL"),
        username=config.get("ADMIN_INIT_LOGIN"),
        password=config.get("ADMIN_INIT_PASSWORD"),
    )
    db.add(default_user)
    db.commit()


if __name__ == "__main__":
    initialize(config.get("SQLALCHEMY_DATABASE_URI"))
    uvicorn.run("main:app", reload=config.get("RELOAD"), host="0.0.0.0", port=10009)

"""
1. Find how to set body's example on OpenAPI3.
3. Write DBOperater`
4. argument_handler use inspect to check is BaseModel
"""
