from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from App.database import Base

class User(Base):
    """
    Model class representing users in the database.

    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Define relationship
    storages = relationship('Storage', back_populates='user', lazy='joined')

    def __repr__(self) -> str:
        """
        Returns a string representation of the User object.

        Returns:
            str: String representation of the User object.
        """
        return f"<User(id={self.id}, username={self.username})>"

    def to_dict(self) -> dict:
        """
        Converts the User object to a dictionary representation.

        Returns:
            dict: Dictionary representation of the User object.
        """
        return {
            "id": self.id,
            "username": self.username
        }
