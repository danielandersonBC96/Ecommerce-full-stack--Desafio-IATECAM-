from sqlalchemy.orm import Session
from app import models, schemas
from app.core.security import get_password_hash

def get_category (db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_categories(db: Session skip: int = 0, limit : int = 10 ):
    return db.query(models.Category).offset(skip).limit(limit).all()

def create_category(db:Session, category: schemas.CategoryCreate):
    db_category = models.Category(description=category.description)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_product(db: Session, product_id: int ):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_product( db: Session , skip: int = 0 , limit: int = 10 ):
    returndb.query(models.Product).offset(skip).limit(Limit).all()
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def create_sale(db : Session, saç: schemas.SaleCreate):
    db_sale = models.Sale(**sale.dict())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

def get_user_by_username(db:Session, username: str)
return db.query(models.User). filter(models.user.username == username).first()

def create_user(db:Session, user:schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    dv_user = models.user(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user