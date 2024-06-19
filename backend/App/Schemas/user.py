from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    password :str

class LoginUser(UserBase):
    password
   
 class RegisterUser(UserBase):
    name:str

class UserCredentials( RegisterUser):
        id: int

    class Config:
        orm_mode = True    
