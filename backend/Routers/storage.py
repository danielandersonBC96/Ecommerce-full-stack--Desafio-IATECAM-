from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from Schemas.SchemaProduct import Product, CreateProduct, UpdateProduct  # Corrigido o import
from Config.database import get_db
from Repositories.RepositoriesProduct import ProductRepository
import httpx

router = APIRouter()

# Função para buscar a cotação do dólar
def fetch_usd_brl_rate():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    
    try:
        response = httpx.get(url)
        response.raise_for_status()
        data = response.json()
        return data['rates']['BRL']
    except httpx.RequestError as e:
        print(f"Erro ao obter a taxa de câmbio: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None

# Função para definir o status do produto
def get_product_status(product):
    if product.quantity_in_stock < 10:
        return "Vermelho"
    elif product.quantity_in_stock <= 15:
        return "Amarelo"
    else:
        return "Verde"

@router.post("/products", response_model=Product)  # Corrigido o caminho da rota
def create_product(product_data: CreateProduct, db: Session = Depends(get_db)):
    product_repo = ProductRepository(db)
    created_product = product_repo.create_product(product_data)
    return created_product

@router.get("/products", response_model=List[Product])  # Corrigido o caminho da rota
def get_all_products(db: Session = Depends(get_db)):
    product_repo = ProductRepository(db)
    products = product_repo.get_all_products()

    usd_brl_rate = fetch_usd_brl_rate()
    if usd_brl_rate is None:
        raise HTTPException(status_code=500, detail="Erro ao buscar a taxa de câmbio")

    for product in products:
        product.price_in_dollar = product.price_in_real / usd_brl_rate
        product.status = get_product_status(product)

    return products

@router.put("/products/{product_id}", response_model=Product)  # Corrigido o caminho da rota
def update_product(product_id: int, product_data: UpdateProduct, db: Session = Depends(get_db)):
    product_repo = ProductRepository(db)
    updated_product = product_repo.update_product(product_id, product_data.dict(exclude_unset=True))
    if not updated_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return updated_product

@router.delete("/products/{product_id}")  # Corrigido o caminho da rota
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product_repo = ProductRepository(db)
    product_repo.delete_product(product_id)
    return {"detail": "Produto deletado"}

@router.get("/products/search", response_model=Optional[Product])  # Corrigido o caminho da rota e o response_model
def search_product_by_name(name: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    product_repo = ProductRepository(db)
    product = product_repo.search_product_by_name(name)

    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    usd_brl_rate = fetch_usd_brl_rate()
    if usd_brl_rate is None:
        raise HTTPException(status_code=500, detail="Erro ao buscar a taxa de câmbio")

    product.price_in_dollar = product.price_in_real / usd_brl_rate
    product.status = get_product_status(product)

    return product

