from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from app.config.database import Base

class SalesByProduct(Base):
    __tablename__ = 'sales_by_product'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False, index=True)
    amount = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    product = relationship('Product', back_populates='sales_by_product', lazy='joined')

    def __repr__(self) -> str:
        return (
            f"<SalesByProduct(id={self.id}, product_id={self.product_id}, "
            f"amount={self.amount}, created_at={self.created_at})>"
        )

    def to_dict(self) -> dict:
      
        return {
            "id": self.id,
            "product_id": self.product_id,
            "amount": self.amount,
            "created_at": self.created_at.isoformat()
        }
