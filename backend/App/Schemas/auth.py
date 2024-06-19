from pydantic import BaseModel


class u UserBase(BaseModel):
    username: str
    password: str

class Login User(UserBase):
    pass

class RegistreUser(UserBase):
    name: str

class UserCredential(RegistreUser):
    id: int

    class Config:
        orm_mode = True

