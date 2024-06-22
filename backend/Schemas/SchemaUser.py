from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    username: str

class CreateUser(UserBase):


    password: str

class UpdateUser(UserBase):
    name:str
    password:str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
