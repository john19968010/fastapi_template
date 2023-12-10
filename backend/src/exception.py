from fastapi import HTTPException


TOKEN_COULD_NOT_VALIDATE = HTTPException(
    status_code=400,
    detail="",
    headers={"WWW-Authenticate": "Bearer"},
)
