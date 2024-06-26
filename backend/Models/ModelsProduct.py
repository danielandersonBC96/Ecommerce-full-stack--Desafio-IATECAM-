from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from Config.database import Base
from Models.ModelsCategory import Category
from Models.ModelsUser import User

class Product(Base):
    """
    Model class representing products in the database.
    """
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    quantity_in_stock = Column(Integer, nullable=False)
    price_in_real = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    # Define relationships
    category = relationship("Category", backref="products")
    storages = relationship('Storage', back_populates='product', lazy='joined')
    sales_by_product = relationship('SalesByProduct', back_populates='product', lazy='joined')
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", backref="products")
   
    def __repr__(self) -> str:
        """
        Returns a string representation of the Product object.
        """
        return (
            f"<Product(id={self.id}, name={self.name}, description={self.description}, "
            f"image_url={self.image_url}, price_in_real={self.price_in_real}, "
            f"category_id={self.category_id}, quantity_in_stock={self.quantity_in_stock})>"
        )

    def to_dict(self) -> dict:
        """
        Converts the Product object to a dictionary representation.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "image_url": self.image_url,
            "quantity_in_stock": self.quantity_in_stock,
            "price_in_real": self.price_in_real,
            "category_id": self.category_id,  # Certifique-se de incluir category_id aqui
            "category": self.category.name if self.category else None,
            "user": self.name_user
        }
