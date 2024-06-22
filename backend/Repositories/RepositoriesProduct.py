from typing import List
from sqlalchemy.orm import Session
from Models.ModelsProduct import Product as ProductModel
from Repositories.main import AbstractRepository
from Schemas.SchemaProduct import Product, CreateProduct, UpdateProduct


class ProductRepository(AbstractRepository[ProductModel]):
    """
    Repository class for handling CRUD operations related to Product entities.
    """

    def __init__(self, db: Session):
        """
        Initializes the ProductRepository with a database session.
        """
        super().__init__(db)
        self.model = ProductModel

    def create_product(self, product: CreateProduct) -> Product:
        """
        Create a new product.

        """
        try:
            entity = ProductModel(name=product.name)
            return self._create(entity)
        except Exception as e:
            self._db.rollback()
            raise e
    
    def get_product_by_id(self, product_id: int) -> Product:
        """
        Retrieve a product by its ID.

        """
        try:
            return self._get(product_id)
        except Exception as e:
            raise e

    def update_product(self, product_id: int, updated_product: UpdateProduct) -> Product:
        """
        Update a product by its ID.

        """
        try:
            product = self._get(product_id)
            if product:
                product.name = updated_product.name
                self._commit()
            return product
        except Exception as e:
            self._db.rollback()
            raise e

    def get_all_products(self) -> List[Product]:
        """
        Retrieve all products.

        """
        try:
            return self._get_all()
        except Exception as e:
            raise e

    def get_product_by_name(self, value: str) -> Product:
        """
        Retrieve a product by its name.

        """
        try:
            return self._search_one_with("name", value)
        except Exception as e:
            raise e
