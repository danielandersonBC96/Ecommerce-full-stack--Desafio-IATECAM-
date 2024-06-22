from pydantic import BaseModel
from Schemas.SchemaProduct import Product

class SalesByProductBase(BaseModel):
    """
    Base schema for SalesByProduct containing common fields.
    """
    amount: int

class CreateSalesByProduct(SalesByProductBase):
    """
    Schema for creating a new SalesByProduct entry. 
    Inherits common fields from SalesByProductBase and adds the product_id.
    """
    product_id: int

class SalesByProduct(SalesByProductBase):
    """
    Detailed schema for SalesByProduct including additional fields like id and the associated product.
    """
    id: int
    product: Product

    class Config:
        orm_mode = True  # Enable compatibility with ORM models
