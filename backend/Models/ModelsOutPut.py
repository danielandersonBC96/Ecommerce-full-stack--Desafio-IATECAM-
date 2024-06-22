from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from Config.database import Base

class Output(Base):
    __tablename__ = 'outputs'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    storage_id = Column(Integer, ForeignKey('storages.id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)

    # Define relationships
    storage = relationship("Storage", back_populates="outputs", lazy="joined", primaryjoin="Output.storage_id == Storage.id")
    user = relationship("User", back_populates="outputs", lazy="joined", primaryjoin="Output.user_id == User.id")

    def __repr__(self) -> str:
        return f"<Output(id={self.id}, amount={self.amount}, created_at={self.created_at}, storage_id={self.storage_id}, user_id={self.user_id})>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "amount": self.amount,
            "created_at": self.created_at.isoformat(),
            "storage_id": self.storage_id,
            "user_id": self.user_id
        }
