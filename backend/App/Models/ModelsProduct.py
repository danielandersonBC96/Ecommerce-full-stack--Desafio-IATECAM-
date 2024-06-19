
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.config.database import Base

class Product(Base):
    """
    Model class representing products in the database.

    """
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    quality = Column(Integer, nullable=False)

    # Define relationships
    category = relationship('Category', back_populates='products', lazy='joined')
    sales_by_product = relationship('SalesByProduct', back_populates='product', lazy='joined')

    def __repr__(self) -> str:
        """
        Returns a string representation of the Product object.

        Returns:
            str: String representation of the Product object.
        """
        return (
            f"<Product(id={self.id}, description={self.description}, "
            f"price={self.price}, category_id={self.category_id}, quality={self.quality})>"
        )

    def to_dict(self) -> dict:
        """
        Converts the Product object to a dictionary representation.

        Returns:
            dict: Dictionary representation of the Product object.
        """
        return {
            "id": self.id,
            "description": self.description,
            "price": self.price,
            "category_id": self.category_id,
            "quality": self.quality
        }
