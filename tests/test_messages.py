from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import DataBase
from app.dependencies import get_db
from app.main import app


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False,
                                   autoflush=False, bind=engine)

DataBase.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app, base_url="http://localhost")

test_message = {"message": "test message"}


def test_create_message():
    response = client.post("/messages/", json=test_message)
    assert response.status_code == 201


def test_read_created_message():
    response = client.get("/messages/")
    assert response.status_code == 200
    assert response.json()[-1]["message"] == test_message["message"]


def test_delete_message():
    response = client.get("/messages/")
    assert response.status_code == 200

    id = response.json()[0]["id"]
    response = client.delete(f"/messages/{id}/")
    assert response.status_code == 204


def test_read_messages_after_delete():
    response = client.get("/messages/")
    assert response.status_code == 200
    assert len(response.json()) == 0
