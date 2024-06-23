# SchemaCategory.py

from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str
    description: str



class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True

class CreateCategory(CategoryBase):
    pass

