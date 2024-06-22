from pydantic import BaseModel
from Schemas.SchemaTag import Tag

class SalesByTagBase(BaseModel):
    """
    Base schema for SalesByTag containing common fields.
    """
    amount: int

class CreateSalesByTag(SalesByTagBase):
    """
    Schema for creating a new SalesByTag entry. 
    Inherits common fields from SalesByTagBase and adds the tag_id.
    """
    tag_id: int

class SalesByTag(SalesByTagBase):
    """
    Detailed schema for SalesByTag including additional fields like id and the associated tag.
    """
    id: int
    tag: Tag

    class Config:
        orm_mode = True  # Enable compatibility with ORM models
