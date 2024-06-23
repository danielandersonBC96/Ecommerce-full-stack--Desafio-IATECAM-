
from pydantic import BaseModel

class PurchaseProduct(BaseModel):
    name: str
    quantity: int


    class Config:
        orm_mode = True
