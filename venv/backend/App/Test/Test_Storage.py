# app/tests/test_storages.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.database import Base, engine, TestingSessionLocal
from app.main import app
from app.models import Storage, Product, Tag, User

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

def test_create_storage(client: TestClient, db_session: Session):
    # Criação dos objetos necessários (Product, Tag, User)
    product = Product(name="Test Product")
    tag = Tag(name="Test Tag")
    user = User(email="testuser@example.com", hashed_password="fakehashedpassword")

    db_session.add(product)
    db_session.add(tag)
    db_session.add(user)
    db_session.commit()

    db_session.refresh(product)
    db_session.refresh(tag)
    db_session.refresh(user)

    # Criação do Storage
    response = client.post("/storages/", json={
        "price": 100.0,
        "description": "Test Storage",
        "amount": 10,
        "product_id": product.id,
        "tag_id": tag.id,
        "user_id": user.id
    })
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 100.0
    assert data["description"] == "Test Storage"
    assert data["amount"] == 10
    assert data["product_id"] == product.id
    assert data["tag_id"] == tag.id
    assert data["user_id"] == user.id

def test_read_storages(client: TestClient, db_session: Session):
    response = client.get("/storages/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
