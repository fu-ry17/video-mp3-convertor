from pydantic import BaseModel

class LoginSchema(BaseModel):
    email: str
    password: str

class RegisterSchema(LoginSchema):
    username: str
