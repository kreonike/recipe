from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Recipe(Base):
    """Модель SQLAlchemy для хранения данных о рецептах."""

    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    cooking_time = Column(Integer, nullable=False)
    ingredients = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    views = Column(Integer, default=0)


class RecipeBase(BaseModel):
    """Базовая модель Pydantic для валидации рецептов."""

    name: str
    cooking_time: int
    ingredients: str
    description: str


class RecipeCreate(RecipeBase):
    """Модель Pydantic для создания нового рецепта."""

    pass


class RecipeList(RecipeBase):
    """Модель Pydantic для списка рецептов с дополнительными полями."""

    id: int
    views: int

    class Config:
        from_attributes = True


class RecipeDetail(RecipeList):
    """Модель Pydantic для детального просмотра рецепта."""

    pass
