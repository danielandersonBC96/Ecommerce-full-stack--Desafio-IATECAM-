from sqlalchemy.orm import Session
from Models.ModelsProduct import Product

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
