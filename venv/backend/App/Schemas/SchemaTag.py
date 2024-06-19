from pydantic import BaseModel

class TagBase(BaseModel):
    """
    Base schema for Tag containing common fields.
    """
    name: str

class CreateTag(TagBase):
    """
    Schema for creating a new Tag.
    Inherits fields from TagBase.
    """
    pass

class UpdateTag(TagBase):
    """
    Schema for updating Tag fields.
    Inherits fields from TagBase.
    """
    pass

class Tag(TagBase):
    """
    Detailed schema for Tag including its ID.
    Inherits fields from TagBase and adds ID field.
    """
    id: int

    class Config:
        orm_mode = True  # Enable compatibility with ORM models
