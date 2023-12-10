from model import User
from datetime import timedelta

from .schemas import LoginFormData
from sqlalchemy.orm import Session
from ..jwt import create_access_token, ACCESS_TOKEN_DAY
from .exception import LOGIN_ERROR


def generate_jwt_token_via_db_row(db_row: User):
    data = {
        "username": db_row.username,
        "email": db_row.email,
    }
    access_token = create_access_token(
        data=data, expires_delta=timedelta(days=ACCESS_TOKEN_DAY)
    )
    return access_token


def login(form: LoginFormData, db: Session):
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
    row = db.query(User).filter_by(username=username, password=password).first()

    if row is None:
        raise LOGIN_ERROR

    return {"data": {"access_token": generate_jwt_token_via_db_row(row)}}
