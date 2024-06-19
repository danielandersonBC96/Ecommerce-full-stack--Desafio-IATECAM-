from sqlalchemy import Column , Interger, String,  ForeignKey , Float 
from sqlalchemy.orm import relationship
from app.databse import Base 

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    storages = relationship('Storage', back_populates='user', lazy='joined')

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username})>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username
        }
