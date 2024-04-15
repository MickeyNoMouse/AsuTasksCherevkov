import pytest
import os
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.model import Base
from public.employees import employees_router
import logging

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

TEST_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def test_db_session():
    logging.debug("Начало теста")
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    logging.debug("Завершение теста")


client = TestClient(employees_router)


def test_get_employees_empty_db(test_db_session):
    logging.debug("Начало теста")
    response = client.get("/employees/show")
    assert response.status_code == 200
    assert response.json() == {"message": "Пользователи не найдены"}
    logging.debug("Завершение теста")


def test_get_employee_not_found(test_db_session):
    logging.debug("Начало теста")
    response = client.get("/employees/show/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Пользователь не найден"}
    logging.debug("Завершение теста")


def test_create_employee(test_db_session):
    logging.debug("Начало теста")
    data = {"item": {"id": 187, "name": "John", "age": 30, "post": "Developer"}}

    response = client.post("/employees/create", json=data)
    assert response.status_code == 200
    assert response.json()["id"] == 187
    assert response.json()["name"] == "John"
    assert response.json()["age"] == 30
    assert response.json()["post"] == "Developer"
    logging.debug("Завершение теста")

if __name__ == "__main__":
    pytest.main(["-v", "--disable-warnings"])
