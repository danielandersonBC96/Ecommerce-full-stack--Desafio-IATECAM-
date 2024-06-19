# app/tests/test_output.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.database import Base, engine, TestingSessionLocal
from app.main import app
from app.models import Output, Storage, User

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

def test_create_output(client: TestClient, db_session: Session):
    # Criação dos objetos necessários (Storage, User)
    storage = Storage(price=10.0, description="Test Storage", amount=100, product_id=1, tag_id=1, user_id=1)
    user = User(username="testuser", email="test@example.com", password="testpassword")
    db_session.add(storage)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(storage)
    db_session.refresh(user)

    # Criação do Output
    response = client.post("/outputs/", json={
        "amount": 10,
        "storage_id": storage.id,
        "user_id": user.id
    })
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 10
    assert data["storage_id"] == storage.id
    assert data["user_id"] == user.id
    assert "id" in data

    # Verify output in the database
    output = db_session.query(Output).filter(Output.storage_id == storage.id).first()
    assert output is not None
    assert output.amount == 10
    assert output.storage_id == storage.id
    assert output.user_id == user.id

def test_read_outputs(client: TestClient, db_session: Session):
    response = client.get("/outputs/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
