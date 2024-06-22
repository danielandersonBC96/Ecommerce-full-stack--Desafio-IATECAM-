
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from Config.database import get_db, create_tables
from Schemas.SchemaUser import User, CreateUser, UpdateUser
from Repositories.RepositoriesUser import UserRepository
import jwt
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

create_tables()  # Chama a função para criar as tabelas ao iniciar a aplicação

@router.get("/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = UserRepository(db).get_all_users(skip=skip, limit=limit)
    return users

@router.post("/", response_model=User)
def create_user(user_data: CreateUser, db: Session = Depends(get_db)):
    # Verifica se os campos necessários estão presentes
    if not user_data.name or not user_data.username or not user_data.password:
        raise HTTPException(status_code=400, detail="Name, username, and password are required")

    # Cria o usuário no banco de dados
    created_user = UserRepository(db).create_user(user_data)

    return created_user

@router.get("/users/{username}", response_model=User)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = UserRepository(db).get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/users/{username}")
def delete_user_by_username(username: str, db: Session = Depends(get_db)):
    UserRepository(db).delete_user_by_username(username)
    return {"message": f"User '{username}' deleted successfully"}

@router.put("/users/{username}")
def update_user_by_username(username: str, updated_user: UpdateUser, db: Session = Depends(get_db)):
    updated_user = UserRepository(db).update_user_by_username(username, updated_user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail=f"User '{username}' not found")
    return updated_user

   