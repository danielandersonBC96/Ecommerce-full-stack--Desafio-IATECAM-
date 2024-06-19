from App.config.session import AppService
from App.Schemas. SchemaSalesTag import CreateSalesByTag, SalesByTag
from App.Repositories.RepositoriesSalesTag import SalesByTagRepository
from typing import List

class SalesByTagService(AppService):
    """
    Service layer for managing sales by tag in the application.

    Attributes:
        db (Session): Database session object.

    Methods:
        create_sales(sales: CreateSalesByTag) -> SalesByTag:
            Creates a new sales record for a tag if it doesn't already exist.
        """

    def create_sales(self, sales: CreateSalesByTag) -> SalesByTag:
        """
        Creates a new sales record for a tag if it doesn't already exist.

        Args:
            sales (CreateSalesByTag): Sales data including tag ID and amount.

        Returns:
            SalesByTag: Created or existing sales record.

        Raises:
            HTTPException: If the sales record with the same tag ID already exists.
        """
        sales_data = SalesByTagRepository(self.db).get_sale_by_tag_id(sales.tag_id)

        if sales_data:
            return sales_data
        
        return SalesByTagRepository(self.db).create_sales_by_tag(sales)

    def get_sales_by_tag(self) -> List[SalesByTag]:
        """
        Retrieves all sales records by tag.

        Returns:
            List[SalesByTag]: List of sales records.
        """
        return SalesByTagRepository(self.db).get_sales_by_tag()

    def add_to_analytics(self, tag_id: int, amount: int) -> SalesByTag:
        """
        Adds sales data to analytics by updating existing or creating new sales record.

        Args:
            tag_id (int): ID of the tag.
            amount (int): Amount of sales to add.

        Returns:
            SalesByTag: Updated or created sales record.
        """
        sale = CreateSalesByTag(tag_id=tag_id, amount=amount)

        sales_data = self.create_sales(sale)

        sales_data.amount += amount

        return sales_data
