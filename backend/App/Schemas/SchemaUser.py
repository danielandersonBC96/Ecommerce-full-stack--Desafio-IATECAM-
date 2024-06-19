from pydantic import BaseModel

class UserBase(BaseModel):
    """
    Base schema for User containing common fields.
    """
    username: str
    password: str

class LoginUser(UserBase):
    """
    Schema for user login.
    Inherits fields from UserBase.
    """
    pass

class RegisterUser(UserBase):
    """
    Schema for registering a new user.
    Inherits fields from UserBase and adds 'name' field.
    """
    name: str

class UserCredentials(RegisterUser):
    """
    Detailed schema for user credentials including ID.
    Inherits fields from RegisterUser and adds 'id' field.
    """
    id: int

    class Config:
        orm_mode = True  # Enable compatibility with ORM models
