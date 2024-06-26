from pydantic import BaseModel
from datetime import datetime
from  Schemas.SchemaUser import User
from Schemas.SchemaStorage import Storage

class Outputs(BaseModel):
    """
    Base schema for Output, containing common fields.
    """
    amount: int

class CreateOutput(Outputs):
    """
    Schema for creating an Output, including storage_id and user_id.
    """
    storage_id: int
    user_id: int

class Output(Outputs):
    """
    Detailed schema for Output, including additional fields like id, user, storage, and created_at.
    """
    id: int
    user: User
    storage: Storage
    created_at: datetime

    class Config:
        orm_mode = True  # Enables compatibility with ORM models
