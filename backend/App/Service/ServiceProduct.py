from fastapi import HTTPException, Response
from app.schemas.product import Product, CreateProduct, UpdateProduct
from app.repositories.product import ProductRepository
from sqlalchemy.orm import Session
from typing import List

from app.services.tag import TagService
from app.config.session import AppService

class ProductService(AppService):
    """
    Service layer for managing products in the application.

    Handles creation, retrieval, updating, and deletion of products.

    """

    def create_product(self, product: CreateProduct) -> Product:
        """
        Creates a new product if it doesn't already exist.

        """
        product_data = ProductRepository(self.db).get_product_by_name(product.name)

        if product_data:
            return product_data
        
        return ProductRepository(self.db).create_product(product)

    def get_product_by_id(self, product_id: int) -> Product:
        """
        Retrieves a product by its ID.

        """
        product_data = ProductRepository(self.db).get_product_by_id(product_id)
        
        if not product_data:
            raise HTTPException(status_code=404, detail="Product not found")

        return product_data

    def update_product_by_id(self, product_id: int, product: UpdateProduct) -> Product:
        """
        Updates a product's name by its ID.

        """
        product_data = self.get_product_by_id(product_id)

        existing_product = ProductRepository(self.db).get_product_by_name(product.name)

        if existing_product and existing_product.id != product_id:
            raise HTTPException(status_code=409, detail="Product with this name already exists")
        
        product_data.name = product.name

        return ProductRepository(self.db).update_product(product_data)

    def delete_product_by_id(self, product_id: int) -> Response:
        """
        Deletes a product by its ID.

        """
        product_data = self.get_product_by_id(product_id)
        
        ProductRepository(self.db).delete_product_by_id(product_data.id)
        
        # Check if the product was successfully deleted
        existing_product = ProductRepository(self.db).get_product_by_id(product_data.id)
        
        if existing_product:
            raise HTTPException(status_code=400, detail="Cannot delete product")

        return Response(status_code=204)
              
    def get_all_products(self) -> List[Product]:
        """
         etrieves all products in the system.

        """
        return ProductRepository(self.db).get_all_products()
