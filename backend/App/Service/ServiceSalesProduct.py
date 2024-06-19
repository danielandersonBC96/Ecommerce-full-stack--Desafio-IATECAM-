from app.config.session import AppService
from App.Schemas.SchemaSalesProduct import CreateSalesByProduct, SalesByProduct
from App.Repositories.RepositoriesProduct import SalesByProductRepository
from typing import List

class SalesByProductService(AppService):
    """
    Service layer for managing sales by product in the application.

    Attributes:
        db (Session): Database session object.

    Methods:
        create_sales(sales: CreateSalesByProduct) -> SalesByProduct:
            Creates a new sales record for a product if it doesn't already exist.
        
    """

    def create_sales(self, sales: CreateSalesByProduct) -> SalesByProduct:
        """
        Creates a new sales record for a product if it doesn't already exist.

        Args:
            sales (CreateSalesByProduct): Sales data including product ID and amount.

        Returns:
            SalesByProduct: Created or existing sales record.

        Raises:
            HTTPException: If the sales record with the same product ID already exists.
        """
        sales_data = SalesByProductRepository(self.db).get_sale_by_product_id(sales.product_id)

        if sales_data:
            return sales_data
        
        return SalesByProductRepository(self.db).create_sales_by_product(sales)
    
    def get_sales_by_product(self) -> List[SalesByProduct]:
        """
        Retrieves all sales records by product.

        Returns:
            List[SalesByProduct]: List of sales records.
        """
        return SalesByProductRepository(self.db).get_sales_by_product()

    def add_to_analytics(self, product_id: int, amount: int) -> SalesByProduct:
        """
        Adds sales data to analytics by updating existing or creating new sales record.

        """
        sale = CreateSalesByProduct(product_id=product_id, amount=amount)

        sales_data = self.create_sales(sale)

        sales_data.amount += amount

        return sales_data
