import os
from urllib import parse as url_parse
from typing import Any
from dotenv import load_dotenv


FIXED = {}


def per_load():
    # Use for local testing
    load_dotenv()
    __sql_url_parsing()


def __sql_url_parsing():
    if "SQLALCHEMY_DATABASE_URI" not in FIXED:
        sql_url = (
            f"postgresql://"
            f'{get("DB_USER")}:'
            f'{url_parse.quote_plus(get("DB_PASSWORD", ""))}@'
            f'{get("DB_HOST")}:{get("DB_PORT")}/'
            f'{get("DB_NAME")}'
        )
        FIXED["SQLALCHEMY_DATABASE_URI"] = sql_url


def get(key: str, default: Any | None = None) -> Any | None:
    env = os.getenv(key)
    if env is not None:
        return env
    elif key in FIXED:
        return FIXED[key]
    else:
        return default


per_load()
