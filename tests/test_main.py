import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app, get_db
from models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_recipe():
    response = client.post(
        "/recipes",
        json={
            "name": "Тестовый рецепт",
            "cooking_time": 30,
            "ingredients": "Ингредиенты",
            "description": "Описание",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Тестовый рецепт"
    assert data["cooking_time"] == 30


def test_read_recipes():
    client.post(
        "/recipes",
        json={
            "name": "Тестовый рецепт",
            "cooking_time": 30,
            "ingredients": "Ингредиенты",
            "description": "Описание",
        },
    )
    response = client.get("/recipes")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == "Тестовый рецепт"


def test_read_recipe():
    response = client.post(
        "/recipes",
        json={
            "name": "Тестовый рецепт",
            "cooking_time": 30,
            "ingredients": "Ингредиенты",
            "description": "Описание",
        },
    )
    recipe_id = response.json()["id"]
    response = client.get(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Тестовый рецепт"
    assert data["views"] == 1
