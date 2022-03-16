from fastapi import Depends
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import models
from httpx import AsyncClient

from app.database.database import DataBase
from app.dependencies import get_db, get_settings
from app.main import app
from .testing_items import testing_items
from .lessons_for_tests import lessons


settings = get_settings()
if settings.debug:
    SQLALCHEMY_DATABASE_URL = "sqlite:///tests/sql_app.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    SQLALCHEMY_DATABASE_URL = settings.test_database_url
    engine = create_engine(SQLALCHEMY_DATABASE_URL)


TestingSessionLocal = sessionmaker(autocommit=False,
                                   autoflush=False, bind=engine)

DataBase.metadata.drop_all(bind=engine)
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


# def test_setting_working_data():



@pytest.mark.asyncio
async def test_refresh():
    response = client.post(
        "/working_data/", headers={"X-Auth-Token": "coneofsilence"}, json={
            "name": "weeks_count",
            "value": "17"
        })
    assert response.status_code == 401
    response = client.post(
        "/working_data/", headers={"X-Auth-Token": settings.app_secret}, json={
            "name": "weeks_count",
            "value": "17"
        })
    assert response.status_code == 200
    assert {"id": 1, "name": "weeks_count", "value": "17"} == response.json()

    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        response = await ac.post("/working_data/refresh/", headers={"X-Auth-Token": "coneofsilence"})
        assert response.status_code == 401
        print("404??!!")
        response = await ac.post("/working_data/refresh/", headers={"X-Auth-Token": settings.app_secret})
        assert response.status_code == 200

    # async with AsyncClient(app=app, base_url="http://localhost") as ac:

    print("await??!!")


def test_calls():
    response = client.get("/calls/")
    assert response.status_code == 200
    assert testing_items["calls"] == response.json()

    response = client.get("/calls/1/")
    assert response.status_code == 200
    assert testing_items["calls"][0] == response.json()

def test_disciplines():
    response = client.get("/disciplines/")
    assert response.status_code == 200
    assert testing_items["disciplines"] == response.json()

    response = client.get("/disciplines/1/")
    assert response.status_code == 200
    assert testing_items["disciplines"][0] == response.json()


def test_degrees():
    response = client.get("/degrees/")
    assert response.status_code == 200
    assert testing_items["degrees"] == response.json()

    response = client.get("/degrees/1/")
    assert response.status_code == 200
    assert testing_items["degrees"][0] == response.json()

def test_lessons():
    response = client.get("/lessons/")
    assert response.status_code == 200
    assert lessons == response.json()

    response = client.get("/lessons/1/")
    assert response.status_code == 200
    assert lessons[0] == response.json()



# def test_read_created_message():
#     response = client.get("/messages/")
#     assert response.status_code == 200
#     assert response.json()[-1]["message"] == test_message["message"]


# def test_delete_message():
#     response = client.get("/messages/")
#     assert response.status_code == 200

#     id = response.json()[0]["id"]
#     response = client.delete(f"/messages/{id}/")
#     assert response.status_code == 204


# def test_read_messages_after_delete():
#     response = client.get("/messages/")
#     assert response.status_code == 200
#     assert len(response.json()) == 0
