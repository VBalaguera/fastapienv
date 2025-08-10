from pydantic import BaseModel, Field
from typing import Optional


class Book(BaseModel):
    id: str
    title: str
    author: str
    category: str
    description: str
    rating: int


def __init__(self, id, title, author, category, description, rating):
    self.id = id
    self.title = title
    self.author = author
    self.category = category
    self.description = description
    self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = Field(decription='Id is not needed on create', default=None)
    title: str = Field(min_length=1, max_length=1000)
    author: str = Field(min_length=1, max_length=1000)
    category: str = Field(min_length=1, max_length=1000)
    description: str = Field(min_length=1, max_length=1000)
    rating: int = Field(gt=-1, lt=11)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A tale of two cities",
                "author": "You know who",
                "description": "a classic",
                "category": "novel",
                "rating": 10
            }
        }
    }

