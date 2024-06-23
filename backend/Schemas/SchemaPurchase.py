
from pydantic import BaseModel

class PurchaseProduct(BaseModel):
    product_id: int
    quantity: int


    class Config:
        orm_mode = True
