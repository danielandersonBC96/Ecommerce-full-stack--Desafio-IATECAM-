from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from Config.database import Base
from Models.ModelsProduct import Product  # Import Product model if not already imported

class SalesByProduct(Base):
    """
    Model class representing sales records by product in the database.

    """
    __tablename__ = 'sales_by_product'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False, index=True)
    amount = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Define relationship
    product = relationship('Product', back_populates='sales_by_product', lazy='joined')

    def __repr__(self) -> str:
        """
        Returns a string representation of the SalesByProduct object.

        Returns:
            str: String representation of the SalesByProduct object.
        """
        return (
            f"<SalesByProduct(id={self.id}, product_id={self.product_id}, "
            f"amount={self.amount}, created_at={self.created_at})>"
        )

    def to_dict(self) -> dict:
        """
        Converts the SalesByProduct object to a dictionary representation.

        Returns:
            dict: Dictionary representation of the SalesByProduct object.
        """
        return {
            "id": self.id,
            "product_id": self.product_id,
            "amount": self.amount,
            "created_at": self.created_at.isoformat()
        }