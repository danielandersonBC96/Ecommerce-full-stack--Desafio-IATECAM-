from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from Config.database import Base

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Relationship to Product
    products = relationship('Product', backref='categories', lazy=True)
