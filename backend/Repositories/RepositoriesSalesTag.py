from typing import List
from sqlalchemy.orm import Session
from  Models.ModelsSalesTags import  Tag as SalesByTagModel
from  Repositories.main import AbstractRepository
from  Schemas.SchemaTag import SalesByTag, CreateTag


class SalesByTagRepository(AbstractRepository[SalesByTagModel]):
    """
    Repository class for handling CRUD operations related to SalesByTag entities.
    """

    def __init__(self, db: Session):
        """
        Initializes the SalesByTagRepository with a database session.
        """
        super().__init__(db)
        self.model = SalesByTagModel

    def create_sale_by_tag(self, sales: CreateTag) -> SalesByTag:
        """
        Create a new sales by tag record.
        """
        try:
            entity = SalesByTagModel(
                tag_id=sales.tag_id,
                amount=0  # Assuming the initial amount is 0, adjust as needed
            )
            return self._create(entity)
        except Exception as e:
            self._db.rollback()
            raise e

    def get_sale_by_tag_id(self, tag_id: int) -> SalesByTag:
        """
        Retrieve a sales by tag record by its tag ID.

        """
        try:
            return self._search_one_with("tag_id", tag_id)
        except Exception as e:
            raise e

    def get_sale_by_tag(self) -> List[SalesByTag]:
        """
        Retrieve all sales by tag records.
        """
        try:
            return self._get_all()
        except Exception as e:
            raise e
