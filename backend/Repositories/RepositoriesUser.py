from sqlalchemy.orm import Session
from fastapi import HTTPException
from Models.ModelsUser import User
from Schemas.SchemaUser import CreateUser, UpdateUser , UserLogin
from Utils.Utils_Hash import Hash
from Config.database import get_db

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: CreateUser) -> User:
        hashed_password = Hash.hash(user_data.password)
        db_user = User(name=user_data.name, username=user_data.username, hashed_password=hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user


    def get_user_by_username(self, username: str) -> User:
        user = self.db.query(User).filter(User.username == username).first()
        return user

    def delete_user_by_username(self, username: str):
        user = self.get_user_by_username(username)
        if user:
            self.db.delete(user)
            self.db.commit()

    def get_all_users(self, skip: int = 0, limit: int = 10):
        return self.db.query(User).all()



    def update_user_by_username(self, username: str, updated_user: UpdateUser):
        user = self.get_user_by_username(username)
        if not user:
            return None
        
        for key, value in updated_user.dict(exclude_unset=True).items():
            setattr(user, key, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user

    def authenticate_user(self, username: str, password: str) -> User:
        user = self.get_user_by_username(username)
        if not user or not Hash.verify(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid username or password")
        return user


 