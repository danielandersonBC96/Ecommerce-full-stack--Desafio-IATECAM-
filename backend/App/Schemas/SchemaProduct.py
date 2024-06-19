from pydantic import BaseModel

class ProductBase(BaseModel):
    """
    Base schema for Product containing common fields.
    """
    name: str

class CreateProduct(ProductBase):
    """
    Schema for creating a new Product. Inherits all fields from ProductBase.
    """
    pass

class UpdateProduct(ProductBase):
    """
    Schema for updating an existing Product. Inherits all fields from ProductBase.
    """
    pass

class Product(ProductBase):
    """
    Detailed schema for Product including additional fields like id.
    """
    id: int

    class Config:
        orm_mode = True  # Enables compatibility with ORM models
