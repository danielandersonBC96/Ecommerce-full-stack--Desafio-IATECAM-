from typing import List
from sqlalchemy.orm import Session
from app.models.storage import Storage as StorageModel
from app.repositories.main import AbstractRepository
from app.schemas.storage import Storage, CreateStorage, UpdateStorage


class StorageRepository(AbstractRepository[StorageModel]):
    """
    Repository class for handling CRUD operations related to Storage entities.
    """

    def __init__(self, db: Session):
        """
        Initializes the StorageRepository with a database session.

        """
        super().__init__(db)
        self.model = StorageModel

    def create_storage(self, storage: CreateStorage) -> Storage:
        """
        Create a new storage record.

        """
        try:
            entity = StorageModel(
                user_id=storage.user_id,
                product_id=storage.product_id,
                tag_id=storage.tag_id,
                price=storage.price,
                description=storage.description,
                amount=storage.amount
            )
            return self._create(entity)
        except Exception as e:
            self._db.rollback()
            raise e

    def get_storage_by_id(self, storage_id: int) -> Storage:
        """
        Retrieve a storage record by its ID.

        """
        try:
            return self._get(storage_id)
        except Exception as e:
            raise e

    def update_storage(self, storage: UpdateStorage) -> Storage:
        """
        Update a storage record.

        """
        try:
            return self._update(storage)
        except Exception as e:
            self._db.rollback()
            raise e

    def delete_storage_by_id(self, storage_id: int) -> None:
        """
        Delete a storage record by its ID.

        """
        try:
            self._delete(storage_id)
        except Exception as e:
            self._db.rollback()
            raise e

    def get_all_storages(self) -> List[Storage]:
        """
        Retrieve all storage records.

        """
        try:
            return self._get_all()
        except Exception as e:
            raise e
    
    def get_all_storages_by_user_id(self, user_id: int) -> List[Storage]:
        """
        Retrieve all storage records belonging to a specific user.

        """
        try:
            return self._search_all_with("user_id", user_id)
        except Exception as e:
            raise e
    
    def get_all_storages_to_buy(self, user_id: int) -> List[Storage]:
        """
        Retrieve all storage records not belonging to a specific user (for buying).

        """
        try:
            return self._search_all_without("user_id", user_id)
        except Exception as e:
            raise e
