import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator, Iterator, List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.models import Base, Recipe, RecipeCreate, RecipeDetail, RecipeList

SQLALCHEMY_DATABASE_URL = "sqlite:///./recipes.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    Base.metadata.create_all(bind=engine)
    yield
    await asyncio.sleep(0)  # Ensure async context
    engine.dispose()


app = FastAPI(
    title="Кулинарная книга API",
    description="API для управления рецептами",
    version="0.29",
    lifespan=lifespan,
)


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/recipes", response_model=List[RecipeList])
async def read_recipes(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[RecipeList]:
    recipes = (
        db.query(Recipe)
        .order_by(Recipe.views.desc(), Recipe.cooking_time.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [RecipeList.model_validate(recipe) for recipe in recipes]


@app.get("/recipes/{recipe_id}", response_model=RecipeDetail)
async def read_recipe(recipe_id: int, db: Session = Depends(get_db)) -> RecipeDetail:
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    db_recipe.views += 1  # Возвращена оригинальная запись
    db.commit()
    db.refresh(db_recipe)
    return RecipeDetail.model_validate(db_recipe)


@app.post("/recipes", response_model=RecipeDetail)
async def create_recipe(
    recipe: RecipeCreate, db: Session = Depends(get_db)
) -> RecipeDetail:
    db_recipe = Recipe(
        name=recipe.name,
        cooking_time=recipe.cooking_time,
        ingredients=recipe.ingredients,
        description=recipe.description,
        views=0,
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return RecipeDetail.model_validate(db_recipe)
