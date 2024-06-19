from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from app.config.database import Base

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    sales_by_tag = relationship('SalesByTag', back_populates='tag', lazy='joined')
    storages = relationship('Storage', back_populates='tag', lazy='joined')

    def __repr__(self) -> str:
        return f"<Tag(id={self.id}, name={self.name})>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name
        }
