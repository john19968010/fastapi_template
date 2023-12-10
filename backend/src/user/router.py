from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from model import get_db
from . import service
from .schemas import LoginResponse, LoginFormData

router = APIRouter(prefix="", tags=["user"])

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Admin login service, return access token \f

    Args:
        * username: str
        * password: str
        db: database session

    Returns:
        access_token: str
    """
    form_data = LoginFormData(username=form_data.username, password=form_data.password)
    return service.login(form_data, db)
