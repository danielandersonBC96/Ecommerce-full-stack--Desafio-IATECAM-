from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    description: str 

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id:Integer

    class Config:

        orm_mode = True

class ProductBase(BaseModel):
    description: str 
    price:  float 
    category_id: int
    quality:int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id:int

    class Config:
        orm_mode = True

class SaleBase(BaseModel):
    product_id: int
    quantity: int

class SaleCreate(SaleBase):
    pass

class Sale (SaleBase):
    id: int

    class Config : 
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True