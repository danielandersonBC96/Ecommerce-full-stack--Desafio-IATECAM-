from pydantic import BaseModel
from datetime import datetime

from app.schemas.user import User
from app.schemas.storage import Storage

class   OutBase(BaseModel):
    amount: int

class CreateOut(OutBase):
    storage_id: int
    user_id: int

class Out( OutBase):
      id: int
    user: User
    storage: Storage
    created_at: datetime
    
        class Config:
        orm_mode = True