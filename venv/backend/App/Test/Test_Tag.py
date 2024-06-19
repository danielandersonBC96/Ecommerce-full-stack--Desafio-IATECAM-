# app/tests/test_tags.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.database import Base, engine, TestingSessionLocal
from app.main import app
from app.models import Tag

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

def test_create_tag(client: TestClient, db_session: Session):
    response = client.post("/tags/", json={"name": "Electronics"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Electronics"
    assert "id" in data

    # Verify tag in the database
    tag = db_session.query(Tag).filter(Tag.name == "Electronics").first()
    assert tag is not None
    assert tag.name == "Electronics"

def test_read_tags(client: TestClient, db_session: Session):
    response = client.get("/tags/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
