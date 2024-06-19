from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from app.config.database import Base

class Output(Base):
    """
    Model class representing the 'outputs' table in the database.
    """

    __tablename__ = 'outputs'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    storage_id = Column(Integer, ForeignKey('storages.id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)

    # Define relationships
    storage = relationship("Storage", back_populates="outputs", lazy="joined")
    user = relationship("User", back_populates="outputs", lazy="joined")

    def __repr__(self) -> str:
        """
        Returns a string representation of the Output object.

        Returns:
            str: String representation of the Output object.
        """
        return f"<Output(id={self.id}, amount={self.amount}, created_at={self.created_at}, storage_id={self.storage_id}, user_id={self.user_id})>"

    def to_dict(self) -> dict:
        """
        Converts the Output object to a dictionary representation.

        Returns:
            dict: Dictionary representation of the Output object.
        """
        return {
            "id": self.id,
            "amount": self.amount,
            "created_at": self.created_at.isoformat(),
            "storage_id": self.storage_id,
            "user_id": self.user_id
        }
