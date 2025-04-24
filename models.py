from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()


class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    cooking_time = Column(Integer, nullable=False)
    ingredients = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    views = Column(Integer, default=0)


class RecipeBase(BaseModel):
    name: str
    cooking_time: int
    ingredients: str
    description: str


class RecipeCreate(RecipeBase):
    pass


class RecipeList(RecipeBase):
    id: int
    views: int

    class Config:
        orm_mode = True


class RecipeDetail(RecipeList):
    pass