
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List


from Schemas.SchemaProduct import Product, CreateProduct, UpdateProduct
from Config.database import get_db
from Repositories.RepositoriesProduct import ProductRepository

router = APIRouter()



# Fetch current USD to BRL exchange rate


@router.post("/", response_model=Product)
def create_product(product_data: CreateProduct, db: Session = Depends(get_db)):
    product_repo = ProductRepository(db)
    created_product = product_repo.create_product(product_data)
    return created_product


@router.get("/", response_model=list[Product])
def get_all_products(db: Session = Depends(get_db)):
    product_repo = ProductRepository(db)
    products = product_repo.get_all_products()

    # Fetch current USD to BRL exchange rate
    usd_brl_rate = fetch_usd_brl_rate()

    for product in products:
        product.price_in_dollar = product.price_in_real / usd_brl_rate

    return products


    for product in products:
        product.price_in_dollar = product.price_in_real / usd_brl_rate
    return products

@router.put("/{product_id}", response_model=Product)
def update_product(product_id: int, product_data: UpdateProduct, db: Session = Depends(get_db)):
    product_repo = ProductRepository(db)
    updated_product = product_repo.update_product(product_id, product_data.dict(exclude_unset=True))
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


@router.put("/{product_id}", response_model=Product)
def update_product(product_id: int, product_data: UpdateProduct, db: Session = Depends(get_db)):
    product_repo = ProductRepository(db)
    updated_product = product_repo.update_product(product_id, product_data)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product
