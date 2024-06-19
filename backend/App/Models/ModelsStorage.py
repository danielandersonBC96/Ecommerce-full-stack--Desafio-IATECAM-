from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.config.database import Base
from App.Models.ModelsProduct import Product  # Import Product model if not already imported
from App.Models.ModelsTag import Tag  # Import Tag model if not already imported
from App.Models.ModelsUser import User  # Import User model if not already imported
from App.Models.ModelsOutput import Output  # Import Output model if not already imported

class Storage(Base):
    """
    Model class representing storage records in the database.

    """
    __tablename__ = 'storages'

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False, index=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)

    # Define relationships
    product = relationship("Product", back_populates="storages", lazy="joined")
    tag = relationship("Tag", back_populates="storages", lazy="joined")
    user = relationship("User", back_populates="storages", lazy="joined")
    outputs = relationship("Output", back_populates="storage", lazy="joined")

    def __repr__(self) -> str:
        """
        Returns a string representation of the Storage object.

        Returns:
            str: String representation of the Storage object.
        """
        return (
            f"<Storage(id={self.id}, price={self.price}, description={self.description}, "
            f"amount={self.amount}, product_id={self.product_id}, tag_id={self.tag_id}, "
            f"user_id={self.user_id})>"
        )

    def to_dict(self) -> dict:
        """
        Converts the Storage object to a dictionary representation.

        Returns:
            dict: Dictionary representation of the Storage object.
        """
        return {
            "id": self.id,
            "price": self.price,
            "description": self.description,
            "amount": self.amount,
            "product_id": self.product_id,
            "tag_id": self.tag_id,
            "user_id": self.user_id
        }
