from sqlalchemy.orm import Session
from Models.ModelsProduct import Product
from Models.ModelsStorage import Storage
from Models.ModelsUser import User
from typing import List, Optional

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, product_data: Product) -> Product:
        db_product = Product(**product_data.dict())
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def get_all_products(self):
        return self.db.query(Product).all()

    def get_product_by_id(self, product_id: int) -> Product:
        return self.db.query(Product).filter(Product.id == product_id).first()

    def update_product(self, product_id: int, updated_data: dict) -> Product:
        product = self.get_product_by_id(product_id)
        if not product:
            return None
        for key, value in updated_data.items():
            setattr(product, key, value)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete_product(self, product_id: int):
        product = self.get_product_by_id(product_id)
        if product:
            self.db.delete(product)
            self.db.commit()

    def search_products_by_name(self, name: str) -> list[Product]:
        return self.db.query(Product).filter(Product.name.ilike(f"%{name}%")).all()
     

    def search_products_by_criteria(self, category_ids: list = None, description: str = None) -> list[Product]:
        query = self.db.query(Product)

        if category_ids:
            query = query.filter(Product.category_id.in_(category_ids))

        if description:
            query = query.filter(Product.description.ilike(f"%{description}%"))

        return query.all()

    
    def reduce_stock(self, product_id: int, quantity: int):
        # Obter o produto do banco de dados
        product = self.get_product_by_id(product_id)

        if not product:
            raise ValueError("Produto não encontrado")

        if quantity <= 0:
            raise ValueError("Quantidade inválida. Deve ser maior que zero.")

        if product.quantity_in_stock == 0:
            raise ValueError("Produto fora de estoque.")

        if quantity > product.quantity_in_stock:
            raise ValueError(f"Quantidade solicitada maior que a disponível em estoque ({product.quantity_in_stock}).")

        # Atualizar a quantidade em estoque
        product.quantity_in_stock -= quantity

        # Verificar se o estoque esgotou
        if product.quantity_in_stock <= 0:
            # Remover o produto do banco de dados se o estoque esgotou
            self.db.delete(product)
        else:
            # Caso contrário, apenas salvar as alterações
            self.db.commit()

        # Retornar o produto atualizado
        return product