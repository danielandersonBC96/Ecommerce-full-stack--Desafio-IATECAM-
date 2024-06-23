from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional,Dict, Any 

from Schemas.SchemaProduct import Product, CreateProduct, UpdateProduct  # Corrigido o import
from Config.database import get_db
import httpx
from Schemas.SchemaCategory import Category,CreateCategory
from Repositories.RepositoriesProduct import ProductRepository
from Repositories.RepositoriesCategory import CategoryRepository 

from Schemas.SchemaPurchase import PurchaseProduct 
from Models.ModelsUser import User

router = APIRouter(

    prefix="/Produtos and Categories",
    tags=["Product and Category"]
)

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


@router.get("/products/search", response_model=List[Product])
def search_product_by_name(name: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    product_repo = ProductRepository(db)
    products = product_repo.search_products_by_name(name)

    if not products:
        raise HTTPException(status_code=404, detail="Produtos não encontrados")

    usd_brl_rate = fetch_usd_brl_rate()
    if usd_brl_rate is None:
        raise HTTPException(status_code=500, detail="Erro ao buscar a taxa de câmbio")

    for product in products:
        product.price_in_dollar = product.price_in_real / usd_brl_rate
        product.status = get_product_status(product)

    return products


@router.post("/categories/", response_model=Category)
def create_category(category_data: CreateCategory, db: Session = Depends(get_db)):
    category_repo = CategoryRepository(db)
    new_category = category_repo.create_category(category_data.name, category_data.description)
    return new_category


    category = products[0].category
    return CategoryResponse(id=category.id, name=category.name, products=products)



@router.get("/products/filte  Cetegories and Description", response_model=List[Product])
def search_products(category_id: Optional[str] = None, description: Optional[str] = None, db: Session = Depends(get_db)):
    product_repo = ProductRepository(db)

    category_ids = None
    if category_id:
        category_ids = [category_id]

    products = product_repo.search_products_by_criteria(category_ids, description)
    return products

@router.post("/{product_name}/purchase", response_model=Product)
def purchase_product_by_name(product_name: str, purchase_data: PurchaseProduct, db: Session = Depends(get_db)):
    product_repo = ProductRepository(db)

    # Buscar o produto pelo nome
    product = product_repo.get_product_by_name(product_name)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    # Verificar se a quantidade desejada está disponível em estoque
    if purchase_data.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantidade inválida. Deve ser maior que zero.")
    if purchase_data.quantity > product.quantity_in_stock:
        raise HTTPException(status_code=400, detail=f"Quantidade solicitada maior que a disponível em estoque ({product.quantity_in_stock}).")

    try:
        # Realizar a compra
        product = product_repo.reduce_stock(product.name, purchase_data.quantity)

        # Se o estoque se esgotou, remover o produto da lista de produtos
        if product.quantity_in_stock <= 0:
            product_repo.delete_product(product.name)

        return product.to_dict()
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno ao processar a compra do produto.")