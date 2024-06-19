from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from app.config.database import Base
from app.models.tag import Tag  # Import Tag model if not already imported

class SalesByTag(Base):
    """
    Model class representing sales records by tag in the database.

    """
    __tablename__ = 'sales_by_tag'

    id = Column(Integer, primary_key=True, index=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), nullable=False, index=True)
    amount = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Define relationship
    tag = relationship("Tag", back_populates="sales_by_tag", lazy="joined")

    def __repr__(self) -> str:
        """
        Returns a string representation of the SalesByTag object.

        Returns:
            str: String representation of the SalesByTag object.
        """
        return (
            f"<SalesByTag(id={self.id}, tag_id={self.tag_id}, "
            f"amount={self.amount}, created_at={self.created_at})>"
        )

    def to_dict(self) -> dict:
        """
        Converts the SalesByTag object to a dictionary representation.

        Returns:
            dict: Dictionary representation of the SalesByTag object.
        """
        return {
            "id": self.id,
            "tag_id": self.tag_id,
            "amount": self.amount,
            "created_at": self.created_at.isoformat()
        }
