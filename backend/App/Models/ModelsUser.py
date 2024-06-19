from sqlalchemy import Column , Interger, String,  ForeignKey , Float 
from sqlalchemy.orm import relationship
from app.databse import Base 

class User(Base):
    __tablename__ =' User'
    id= Column(Integer, primary_Key=True, index =True)
    username = Column(String, unique=True, index=True)
    email = Column( String, unique=True , index = True)
    hashed_password = Column(String)
    is_active = Column(Boolean , default= True)
    
    storages = relationship('Storage', back_populates='user')
    outputs = relationship('Output', back_populates='user')