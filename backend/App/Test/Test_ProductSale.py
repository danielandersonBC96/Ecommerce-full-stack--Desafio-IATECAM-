# app/tests/test_sales_by_product.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.database import Base, engine, TestingSessionLocal
from app.main import app
from app.models import SalesByProduct, Product

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

def test_create_sales_by_product(client: TestClient, db_session: Session):
    # Criação do objeto necessário (Product)
    product = Product(name="Test Product")
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    # Criação do SalesByProduct
    response = client.post("/sales_by_product/", json={
        "product_id": product.id,
        "amount": 10
    })
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == product.id
    assert data["amount"] == 10
    assert "id" in data

    # Verify sales_by_product in the database
    sale = db_session.query(SalesByProduct).filter(SalesByProduct.product_id == product.id).first()
    assert sale is not None
    assert sale.product_id == product.id
    assert sale.amount == 10

def test_read_sales_by_product(client: TestClient, db_session: Session):
    response = client.get("/sales_by_product/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
