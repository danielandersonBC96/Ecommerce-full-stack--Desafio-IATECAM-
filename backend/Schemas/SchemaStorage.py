from pydantic import BaseModel, conint
from  Schemas.SchemaProduct import Product
from Schemas. SchemaTag import Tag
from Schemas. SchemaUser import User

class StorageBase(BaseModel):
    """
    Base schema for storage containing common fields.
    """
    price: float
    description: str
    amount: conint(ge=0)  # amount should be a non-negative integer

class RequestStorage(StorageBase):
    """
    Schema for requesting storage creation. 
    Includes additional fields for product and tag names.
    """
    product_name: str
    tag_name: str

class CreateStorage(StorageBase):
    """
    Schema for creating storage with necessary foreign keys.
    Inherits fields from StorageBase and adds user, product, and tag IDs.
    """
    user_id: int
    product_id: int
    tag_id: int

class UpdateStorage(BaseModel):
    """
    Schema for updating storage fields.
    All fields are optional.
    """
    price: float = None
    description: str = None
    amount: conint(ge=0) = None  # amount should be a non-negative integer

class Storage(StorageBase):
    """
    Detailed schema for storage including related objects.
    Inherits fields from StorageBase and adds IDs and related models.
    """
    id: int
    product: Product
    tag: Tag
    user: User

    class Config:
        orm_mode = True  # Enable compatibility with ORM models
