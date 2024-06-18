from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.Sale)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    product = crud.get_product(db, sale.product_id)
    if product.quantity < sale.quantity:
        raise HTTPException(status_code=400, detail="Insufficient quantity in stock")
    return crud.create_sale(db, sale)