
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from Config.database import get_db
from Service.ServiceSalesProduct import SalesByProductService

from Schemas.SchemaSalesProduct import SalesByProduct
from typing import List

from Schemas.SchemaSalesTag import SalesByTag

from Service.ServiceSalesTag import SalesByTagService

from Middlewares.MiddlewaresAuth import get_current_user

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

@router.get("/sales/by/product", response_model=List[SalesByProduct])
def get_sales_by_product(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)) -> List[SalesByProduct]:
    return SalesByProductService(db).get_sales_by_product()

@router.get("/sales/by/tag", response_model=List[SalesByTag])
def get_sales_by_tag(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)) -> List[SalesByTag]:
    return SalesByTagService(db).get_sales_by_tag()