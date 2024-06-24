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

    def search_products_by_name(self, name: str) -> List[Product]:
        return self.db.query(Product).filter(Product.name.ilike(f"%{name}%")).all()
     
    def search_products_by_criteria(self, category_ids: List[int] = None, description: str = None) -> List[Product]:
        query = self.db.query(Product)

        if category_ids:
            query = query.filter(Product.category_id.in_(category_ids))

        if description:
            query = query.filter(Product.description.ilike(f"%{description}%"))

        return query.all()

    def get_product_by_name(self, product_name: str) -> Product:
        return self.db.query(Product).filter(Product.name == product_name).first()

    def reduce_stock(self, product_name: str, quantity: int, user_id: int) -> Product:
        # Obter o produto do banco de dados pelo nome
        product = self.get_product_by_name(product_name)

        if not product:
            raise ValueError("Produto não encontrado")

        if quantity <= 0:
            raise ValueError("Quantidade inválida. Deve ser maior que zero.")

        if product.quantity_in_stock == 0:
            raise ValueError("Produto fora de estoque.")

        if quantity > product.quantity_in_stock:
            raise ValueError(f"Quantidade solicitada maior que a disponível em estoque ({product.quantity_in_stock}).")

        try:
            # Atualizar a quantidade em estoque
            product.quantity_in_stock -= quantity

            # Criar um novo registro de compra na tabela 'storages'
            storage = Storage(
                price=product.price_in_real,
                description=product.description,
                amount=quantity,
                product_id=product.id,
                tag_id=1,  # Ajuste este valor conforme necessário
                user_id=user_id
            )
            self.db.add(storage)

            # Verificar se o estoque esgotou
            if product.quantity_in_stock <= 0:
                # Remover o produto do banco de dados se o estoque esgotou
                self.db.delete(product)
            else:
                # Caso contrário, apenas salvar as alterações
                self.db.commit()

            # Salvar a transação na tabela 'storages'
            self.db.commit()

            # Retornar o produto atualizado
            return product
        except Exception as e:
            self.db.rollback()
            raise e
