from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from Config.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String)
    name = Column(String)
    storages = relationship('Storage', back_populates='user', lazy='joined')
    outputs = relationship('Output', back_populates='user', lazy='joined', primaryjoin="User.id == Output.user_id")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username})>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name  # Certifique-se de incluir 'name' no dicionário
        }