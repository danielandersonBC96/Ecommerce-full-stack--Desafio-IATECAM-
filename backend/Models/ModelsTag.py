from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from Config.database import Base

class Tag(Base):
    """
    Model class representing tags in the database.

    Attributes:
        id (int): Primary key identifier for the tag.
        name (str): Name of the tag (unique and not nullable).

    Relationships:
        sales_by_tag (Relationship): One-to-many relationship with SalesByTag model.
        storages (Relationship): One-to-many relationship with Storage model.
    """
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # Define relationships
    sales_by_tag = relationship('SalesByTagModels', back_populates='tag', lazy='dynamic')
    storages = relationship('Storage', back_populates='tag', lazy='dynamic')

    def __repr__(self) -> str:
        """
        Returns a string representation of the Tag object.

        Returns:
            str: String representation of the Tag object.
        """
        return f"<Tag(id={self.id}, name={self.name})>"

    def to_dict(self) -> dict:
        """
        Converts the Tag object to a dictionary representation.

        Returns:
            dict: Dictionary representation of the Tag object.
        """
        return {
            "id": self.id,
            "name": self.name
        }
