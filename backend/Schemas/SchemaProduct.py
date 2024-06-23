from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: str
    quantity_in_stock: int
    price_in_real: float
    category_id: str
    image_url: Optional[str]  # Adicionando image_url como uma propriedade opcional

class CreateProduct(ProductBase):
    pass

class UpdateProduct(ProductBase):
    pass

class Product(ProductBase):
    id: int
    available: Optional[bool] = True  # Campo opcional para indicar disponibilidade do produto

    class Config:
        orm_mode = True
