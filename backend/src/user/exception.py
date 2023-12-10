from fastapi import HTTPException


LOGIN_ERROR = HTTPException(status_code=401, detail="Incorrect username or password")
