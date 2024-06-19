from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from app.config.database import Base

class SalesByTag(Base):
    __tablename__ = 'sales_by_tag'

    id = Column(Integer, primary_key=True, index=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), nullable=False, index=True)
    amount = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    tag = relationship("Tag", back_populates="sales_by_tag", lazy="joined")

    def __repr__(self) -> str:
        return (
            f"<SalesByTag(id={self.id}, tag_id={self.tag_id}, "
            f"amount={self.amount}, created_at={self.created_at})>"
        )

    def to_dict(self) -> dict:
      
        return {
            "id": self.id,
            "tag_id": self.tag_id,
            "amount": self.amount,
            "created_at": self.created_at.isoformat()
        }
