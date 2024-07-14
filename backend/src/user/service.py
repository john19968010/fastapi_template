from datetime import timedelta

from .schemas import LoginFormData
import config
from ..jwt import create_access_token, ACCESS_TOKEN_DAY
from .exception import LOGIN_ERROR


def generate_jwt_token_via_db_row():
    data = {
        "username": config.get("ADMIN_INIT_LOGIN"),
        "email": config.get("ADMIN_INIT_EMAIL"),
    }
    access_token = create_access_token(
        data=data, expires_delta=timedelta(days=ACCESS_TOKEN_DAY)
    )
    return access_token


def login(form: LoginFormData):
    """
    Args:
        form_data: User login form data
            * username: str
            * password: str
        db: database session

    Returns:
        access_token: str
    """
    username, password = form.username, form.password

    if username != config.get("ADMIN_INIT_LOGIN") or password != config.get("ADMIN_INIT_PASSWORD"):
        raise LOGIN_ERROR

    return {"data": {"access_token": generate_jwt_token_via_db_row()}}
