from pydantic import BaseModel, Field
from typing import Optional


class Book(BaseModel):
    id: str
    title: str
    author: str
    category: str
    description: str
    rating: float
    published_date: int


class BookRequest(BaseModel):
    title: str = Field(min_length=1, max_length=1000)
    author: str = Field(min_length=1, max_length=1000)
    category: str = Field(min_length=1, max_length=1000)
    description: str = Field(min_length=1, max_length=1000)
    rating: float = Field(gt=-1, lt=11)
    published_date: int = Field(gt=0, lt=2100)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A Tale of Two Cities",
                "author": "Someone",
                "description": "A classic novel",
                "category": "novel",
                "rating": 9.5,
                "published_date": 2010
            }
        }
    }