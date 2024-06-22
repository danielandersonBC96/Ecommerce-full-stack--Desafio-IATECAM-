# app/tests/test_sales_by_tag.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.database import Base, engine, TestingSessionLocal
from app.main import app
from app.models import SalesByTag, Tag

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

def test_create_sales_by_tag(client: TestClient, db_session: Session):
    # Criação do objeto necessário (Tag)
    tag = Tag(name="Test Tag")
    db_session.add(tag)
    db_session.commit()
    db_session.refresh(tag)

    # Criação do SalesByTag
    response = client.post("/sales_by_tag/", json={
        "tag_id": tag.id,
        "amount": 5
    })
    assert response.status_code == 200
    data = response.json()
    assert data["tag_id"] == tag.id
    assert data["amount"] == 5
    assert "id" in data

    # Verify sales_by_tag in the database
    sale = db_session.query(SalesByTag).filter(SalesByTag.tag_id == tag.id).first()
    assert sale is not None
    assert sale.tag_id == tag.id
    assert sale.amount == 5

def test_read_sales_by_tag(client: TestClient, db_session: Session):
    response = client.get("/sales_by_tag/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
