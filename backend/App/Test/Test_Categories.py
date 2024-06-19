
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from app.models import Category
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

def test_create_category(client: TestClient, test_db: Session):
    response = client.post("/categories/", json={"description": "Electronics"})
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Electronics"
    assert "id" in data

def test_read_categories(client: TestClient, test_db: Session):
    response = client.get("/categories/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
