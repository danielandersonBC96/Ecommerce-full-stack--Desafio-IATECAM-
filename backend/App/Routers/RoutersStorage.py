from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from App.config.database import get_db
from App.Service.ServiceStorage import StorageService
from App.Schemas.SchemasStorage import Storage, CreateStorage, UpdateStorage, RequestStorage
from App.Middlewares.MiddlewaresAuth import get_current_user

router = APIRouter(
    prefix="/storages",
    tags=["Storage"]
)

# Endpoint to create a new storage entry
@router.post("/", response_model=Storage, tags=["Storages"])
def create_storage(storage_data: RequestStorage,db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    """
    Create a new storage entry.

    """
    return StorageService(db).create_storage(storage_data, current_user["user_id"])

# Endpoint to get all storages owned by the current user
@router.get("/by/me", response_model=List[Storage])
def get_all_user_storages(db: Session = Depends(get_db),current_user: dict = Depends(get_current_user),skip: int = Query(0, description="Skip first N results for pagination"),limit: int = Query(10, description="Limit number of results per page")):
    """
    Retrieve all storages owned by the current user.

    """
    return StorageService(db).get_all_storages_by_user_id(current_user["user_id"], skip=skip, limit=limit)

# Endpoint to get all storages available for purchase by the current user
@router.get("/to/me", response_model=List[Storage])
def get_all_storages_to_buy(
    db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), skip: int = Query(0, description="Skip first N results for pagination"),limit: int = Query(10, description="Limit number of results per page")
):
    """
    Retrieve all storages available for purchase by the current user.
   
    """
    return StorageService(db).get_all_storages_to_buy(current_user["user_id"], skip=skip, limit=limit)
