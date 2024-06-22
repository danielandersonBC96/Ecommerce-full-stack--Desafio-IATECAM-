# SchemaTag.py

from pydantic import BaseModel

# SchemaTag.py



class Tag(BaseModel):
    id: int
    name: str

class SalesByTag(BaseModel):
    id: int
    tag_name: str

class CreateTag(BaseModel):
    tag_name: str
