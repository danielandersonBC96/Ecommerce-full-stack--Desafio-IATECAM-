from typing import List
from sqlalchemy.orm import Session
from app.models.sales_by_product import SalesByProduct as SalesByProductModel
from app.repositories.main import AbstractRepository
from app.schemas.sales_by_product import SalesByProduct, CreateSalesByProduct


class SalesByProductRepository(AbstractRepository[SalesByProductModel]):
    """
    Repository class for handling CRUD operations related to SalesByProduct entities.
    """

    def __init__(self, db: Session):
        """
        Initializes the SalesByProductRepository with a database session.

        """
        super().__init__(db)
        self.model = SalesByProductModel

    def create_sale_by_product(self, sale: CreateSalesByProduct) -> SalesByProduct:
        """
        Create a new sales by product record.

        """
        try:
            entity = SalesByProductModel(
                product_id=sale.product_id,
                amount=0  # Assuming the initial amount is 0, adjust as needed
            )
            return self._create(entity)
        except Exception as e:
            self._db.rollback()
            raise e

    def get_sale_by_product_id(self, product_id: int) -> SalesByProduct:
        """
        Retrieve a sales by product record by its product ID.

        """
        try:
            return self._search_one_with("product_id", product_id)
        except Exception as e:
            raise e

    def get_sales_by_product(self) -> List[SalesByProduct]:
        """
        Retrieve all sales by product records.

        """
        try:
            return self._get_all()
        except Exception as e:
            raise e
