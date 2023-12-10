from pydantic import BaseModel


# Response
class LoginFormData(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    data: dict
