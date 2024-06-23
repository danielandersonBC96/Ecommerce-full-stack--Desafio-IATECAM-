from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from Config.database import Base

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)  # A coluna de descrição deve ser definida aqui

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name}, description={self.description})>"
        
        products = relationship("Product", secondary=association_table, backref="categories")