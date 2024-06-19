from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter()

@router.post("/", response_model= Storage)
def create_storage( storage_data: RequestStorage, db: Session = Depends(get_db), current_user: disct = Depends(get_current_user)):
    return StorageService(db).create_storage(storage_data, current_user["user_ID"])

@router.get('/by/me', response_model=List[Storage])
def get_all_current_user(db: Session = Depends(get_db), current_user: disct = Depends(get_all_current_user)):
    return  StorageService(db).get_all_storage_by_user_id( current_user["User_id"])

@router.get("/to/me", response_model=List[Storage])
def get_all_storage_to_buy(db: Session = Depends(get_db),current_user:disct = Depends(get_all_current_user)):
    return StorageService(db).get_all_storage_to_buy(current_user["user_id"])
