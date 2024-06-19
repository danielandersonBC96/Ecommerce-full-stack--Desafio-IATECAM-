from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from App.config.database import get_db
from App.Service.ServiceSalesProdutuct import SalesByProductService
from App.Schemas.SchemaSalesProduct import SalesByProduct
from App.Service.SchemaSalesTag import SalesByTagService
from App.Schemas.SchemaSalesTag import SalesByTag
from App.Middlewares.MiddlewaresAuth import get_current_user

#Intace of the Analitics  service to handle business logic
auth_service = AuthService()

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

#Create endpoint for ales data grouped by product.
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

#Create endpoint for sales data grouped by tag.
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
