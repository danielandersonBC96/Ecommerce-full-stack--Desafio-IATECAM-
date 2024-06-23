from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from Config.database import Base
from Models.ModelsCategory import Category

class Product(Base):
    """
    Model class representing products in the database.
    """
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    image_url = Column(String)  # Coluna para armazenar a URL da imagem externa
    quantity_in_stock = Column(Integer)
    price_in_real = Column(Float)
    category_id = Column(String, ForeignKey('categories.id'))

    # Define relationships
    category = relationship("Category", backref="products")
    storages = relationship('Storage', back_populates='product', lazy='joined')
    sales_by_product = relationship('SalesByProduct', back_populates='product', lazy='joined')

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
            "category": self.category.name if self.category else None,  
        }
