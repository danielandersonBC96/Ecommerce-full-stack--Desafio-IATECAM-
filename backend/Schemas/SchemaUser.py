from pydantic import BaseModel

class CreateUser(BaseModel):
    name: str
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    name: str
    username: str

class UpdateUser(BaseModel):
    name:str
    password:str

    class Config:
        orm_mode = True
