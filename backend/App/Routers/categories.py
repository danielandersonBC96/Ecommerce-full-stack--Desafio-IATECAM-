from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Category)
return crud_category(db=db , category =category)

@router.get("/", response_model=list[schemas.category])
def read_categories( skip: int = 0 , limit: int = 10 , db: Session = Depends(get_db)):
    return crud.get_categories(db=db, skip=skip, limit=limit)