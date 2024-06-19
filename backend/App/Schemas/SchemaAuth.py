from pydantic import BaseModel, Field

class UserBase(BaseModel):
    """
    Base model for user, containing common fields.
    """
    username: str = Field(..., example="user123")
    password: str = Field(..., example="securepassword")

class LoginUser(UserBase):
    """
    Model for user login, inherits from UserBase.
    """
    pass

class RegisterUser(UserBase):
    """
    Model for user registration, includes an additional name field.
    """
    name: str = Field(..., example="John Doe")

class UserCredential(RegisterUser):
    """
    Model for user credentials, includes ID and inherits from RegisterUser.
    """
    id: int = Field(..., example=1)

    class Config:
        orm_mode = True  # Enables ORM mode for compatibility with SQLAlchemy models
