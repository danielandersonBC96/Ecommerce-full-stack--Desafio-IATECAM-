from sqlalchemy import Column , Interger, String,  ForeignKey , Float 
from sqlalchemy.orm import relationship
from app.databse import Base 

class  Product(Base):
    __tablename__  = ' products'
    id = Column (Integer, primary_Key=True, index=True) 
    description = Column( String, index=True)
    price = Column(Float)
    Category_id = Column(Integer, ForeignKey('category.id'))    
    quality = Column(Integer)
    category =  relationship('Category')
