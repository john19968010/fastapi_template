import os
from urllib import parse as url_parse
from typing import Any
from dotenv import load_dotenv


FIXED = {}


def per_load():
    # Use for local testing
    load_dotenv()


def get(key: str, default: Any | None = None) -> Any | None:
    env = os.getenv(key)
    if env is not None:
        return env
    elif key in FIXED:
        return FIXED[key]
    else:
        return default


per_load()
