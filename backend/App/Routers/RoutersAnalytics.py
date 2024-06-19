from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.services.sales_by_product import SalesByProductService
from app.schemas.sales_by_product import SalesByProduct
from app.services.sales_by_tag import SalesByTagService
from app.schemas.sales_by_tag import SalesByTag
from app.middlewares.auth import get_current_user

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

@router.get("/sales/by/product", response_model=List[SalesByProduct])
def get_sales_by_product(
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
) -> List[SalesByProduct]:
    """
    Retrieve sales data grouped by product.

    """
    try:
        return SalesByProductService(db).get_sales_by_product()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/sales/by/tag", response_model=List[SalesByTag])
def get_sales_by_tag(
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
) -> List[SalesByTag]:
    """
    Retrieve sales data grouped by tag.

    """
    try:
        return SalesByTagService(db).get_sales_by_tag()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
