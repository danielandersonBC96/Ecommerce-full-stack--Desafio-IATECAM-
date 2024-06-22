from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: str
    quantity_in_stock: int
    price_in_real: float
    category_id: int

class CreateProduct(ProductBase):
    pass

class UpdateProduct(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True
