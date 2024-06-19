
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from app.models import Product, Category
from sqlalchemy.orm import Session

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_create_product(client: TestClient, test_db: Session):
    category = Category(description="Electronics")
    test_db.add(category)
    test_db.commit()
    test_db.refresh(category)
    
    response = client.post("/products/", json={
        "description": "Smartphone",
        "price": 699.99,
        "category_id": category.id,
        "stock_quantity": 100
    })
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Smartphone"
    assert data["price"] == 699.99
    assert data["category_id"] == category.id
    assert data["stock_quantity"] == 100

def test_read_products(client: TestClient, test_db: Session):
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
