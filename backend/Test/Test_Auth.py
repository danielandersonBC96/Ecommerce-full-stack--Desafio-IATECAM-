# app/tests/test_auth.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.database import Base, engine, TestingSessionLocal
from app.main import app
from app.schemas import UserCreate
from app.crud import get_user_by_email

@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def db_session():
    db = TestingSessionLocal()
    yield db
    db.close()

def test_create_user(client: TestClient, db_session: Session):
    response = client.post("/users/", json={"email": "testuser@example.com", "password": "testpassword"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert "id" in data

    # Verify user in the database
    user = get_user_by_email(db_session, email="testuser@example.com")
    assert user is not None
    assert user.email == "testuser@example.com"

def test_user_authentication(client: TestClient):
    # First, create a user
    client.post("/users/", json={"email": "testuser2@example.com", "password": "testpassword"})
    
    # Then, authenticate the user
    response = client.post("/token/", data={"username": "testuser2@example.com", "password": "testpassword"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
