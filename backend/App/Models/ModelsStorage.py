from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.config.database import Base

class Storage(Base):
   
    __tablename__ = 'storages'

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False, index=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)

    product = relationship("Product", back_populates="storages", lazy="joined")
    tag = relationship("Tag", back_populates="storages", lazy="joined")
    user = relationship("User", back_populates="storages", lazy="joined")
    outputs = relationship("Output", back_populates="storage", lazy="joined")

    def __repr__(self) -> str:
        return (
            f"<Storage(id={self.id}, price={self.price}, description={self.description}, "
            f"amount={self.amount}, product_id={self.product_id}, tag_id={self.tag_id}, "
            f"user_id={self.user_id})>"
        )

    def to_dict(self) -> dict:
      
        return {
            "id": self.id,
            "price": self.price,
            "description": self.description,
            "amount": self.amount,
            "product_id": self.product_id,
            "tag_id": self.tag_id,
            "user_id": self.user_id
        }
