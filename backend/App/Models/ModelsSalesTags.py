from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime

from sqlalchemy.orm import relationship

from app.config.database import Base

class SalesByTag(Base):
    __tablename__ = 'salesTag'

    id = Column(Integer, primary_key=True, index=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), index=True)
    amount = Column(Integer, nullable=False)

    tag = relationship("Tag", back_populates="SalesTag", lazy="joined")