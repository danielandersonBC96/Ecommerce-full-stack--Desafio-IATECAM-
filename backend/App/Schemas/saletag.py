from pydantic import BaseModel
from app.schemas.tag import Tag


class salesByBase(BaseModel):
    amount:int

class CreateSalesByTag(CreateSalesByTag):
    tag_id: int 

class SalesByTag(SalesByTagBase):
    id:  tag
    tag: Tag

    class Config:
         orm_mode = True
