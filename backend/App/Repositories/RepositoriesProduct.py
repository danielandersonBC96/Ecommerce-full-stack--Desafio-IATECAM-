from sqlalchemy.orm import Session
from app.models.product import Product as ProductModel
from app.repositories.main import AbstractRepository
from app.schemas.product import Product, CreateProduct, UpdateProduct

from typing import List

class ProductRepository(AbstractRepository[ProductModel]):
     def __init__(self, db: Session):
        super().__init__(db)
        self.model = ProductModel

    def create_product(self,product: CreateProduct) -> Product:
        entity =  ProductModel(name=product.name)
        return self._create(entity)
    
    def get_product_by_id(self, product_id:int) -> Product:
        return self._get(product_id)

    def update_product(self, product_id: int ) -> None:
        return self._delete(product_id)

    def get_all_product(self) -> List[Product]:
        return self._get_all()

    def ger_product_by_name(self, value: str) -> Product:
        return self._search_one_whit("name", value)
