from fastapi import HTTPException, Response
from typing import List

from Schemas.SchemaStorage import Storage, CreateStorage, UpdateStorage, StorageBase, RequestStorage
from Schemas.SchemaProduct import CreateProduct
from Schemas.SchemaTag import CreateTag

from Repositories.RepositoriesStorage import StorageRepository
from sqlalchemy.orm import Session

from Service.ServiceProduct import ProductService
from Service.ServiceTag import TagService

from Config.session import AppService

class StorageService(AppService):
    """
    Service layer for managing storage operations.

    Attributes:
        db (Session): Database session object.

    
    """

    def create_storage(self, storage: RequestStorage, user_id: int) -> Storage:
        """
        Creates a new storage entry with associated product and tag.

        Args:
            storage (RequestStorage): Storage data including product and tag names.
            user_id (int): ID of the user creating the storage entry.

        Returns:
            Storage: Created storage entry.

        Raises:
            HTTPException: If the associated product or tag cannot be created or found.
        """
        product = CreateProduct(name=storage.product_name)
        tag = CreateTag(name=storage.tag_name)

        product_data = ProductService(self.db).create_product(product)
        tag_data = TagService(self.db).create_tag(tag)

        storage_data = CreateStorage(
            user_id=user_id,
            product_id=product_data.id,
            tag_id=tag_data.id,
            price=storage.price,
            description=storage.description,
            amount=storage.amount
        )

        return StorageRepository(self.db).create_storage(storage_data)

    def get_storage_by_id(self, storage_id: int) -> Storage:
        """
        Retrieves a storage entry by its ID.

        Args:
            storage_id (int): ID of the storage entry.

        Returns:
            Storage: Retrieved storage entry.

        Raises:
            HTTPException: If the storage entry with the specified ID is not found.
        """
        storage_data = StorageRepository(self.db).get_storage_by_id(storage_id)
        
        if not storage_data:
            raise HTTPException(status_code=404, detail="Storage not found")

        return storage_data

    def update_storage_by_id(self, storage_id: int, storage: UpdateStorage) -> Storage:
        """
        Updates a storage entry's details.

        Args:
            storage_id (int): ID of the storage entry to update.
            storage (UpdateStorage): Updated storage data.

        Returns:
            Storage: Updated storage entry.

        Raises:
            HTTPException: If the storage entry with the specified ID is not found.
        """
        storage_data = self.get_storage_by_id(storage_id)

        storage_data.price = storage.price if storage.price is not None else storage_data.price
        storage_data.description = storage.description if storage.description is not None else storage_data.description

        return StorageRepository(self.db).update_storage(storage_data)

    def delete_storage_by_id(self, storage_id: int) -> Response:
        """
        Deletes a storage entry by its ID.

        Args:
            storage_id (int): ID of the storage entry to delete.

        Returns:
            Response: HTTP response indicating success (status code 204) or failure.

        Raises:
            HTTPException: If the storage entry with the specified ID cannot be deleted.
        """
        storage_data = self.get_storage_by_id(storage_id)
        
        StorageRepository(self.db).delete_storage_by_id(storage_data.id)
        
        existing_storage = StorageRepository(self.db).get_storage_by_id(storage_id)
        
        if existing_storage:
            raise HTTPException(status_code=400, detail="Can't delete storage")
        
        return Response(status_code=204)

    def get_all_storages(self) -> List[Storage]:
        """
        Retrieves all storage entries.

        Returns:
            List[Storage]: List of all storage entries.
        """
        return StorageRepository(self.db).get_all_storages()
    
    def get_all_storages_by_user_id(self, user_id: int) -> List[Storage]:
        """
        Retrieves all storage entries belonging to a specific user.

        Args:
            user_id (int): ID of the user.

        Returns:
            List[Storage]: List of storage entries belonging to the user.
        """
        return StorageRepository(self.db).get_all_storages_by_user_id(user_id)
    
    def get_all_storages_to_buy(self, user_id: int) -> List[Storage]:
        """
        Retrieves storage entries available for purchase (amount > 0).

        Args:
            user_id (int): ID of the user.

        Returns:
            List[Storage]: List of storage entries available for purchase.
        """
        products = StorageRepository(self.db).get_all_storages_to_buy(user_id)
        filtered_products = [product for product in products if product.amount > 0]
        return filtered_products
