from pydantic import BaseModel, Field

class UserBase(BaseModel):
    username: str
    password: str

class LoginUser(UserBase):
    pass

class CreateUser(BaseModel):
    name: str
    username: str
    password: str

class RegisterUser(CreateUser):
    pass

class UserCredentials(RegisterUser):
    id: int
