from sqlalchemy.orm import Session
from Models.ModelsCategory import Category
from Models.ModelsProduct import Product

class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_category(self, name: str, description: str):
        new_category = Category(name=name, description=description)
        self.db.add(new_category)
        self.db.commit()
        self.db.refresh(new_category)
        return new_category
    
    def get_category_by_name(self, category_name: str):
        return self.db.query(Category).filter(Category.name == category_name).first()
        
    def get_products_by_categories(self, category_name: str) -> list[Product]:
        return self.db.query(Product).filter(Product.category_id.ilike(f"%{category_name}%")).all()