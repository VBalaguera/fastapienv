from pydantic import BaseModel, Field
from typing import Optional


# --- PRODUCT MODELS ---
class Product(BaseModel):
    id: str
    name: str
    brand: str
    price: float
    stock: int
    category: str
    weight: Optional[str]
    additional_notes: Optional[str]

class ProductRequest(BaseModel):
    name: str = Field(min_length=1)
    brand: str = Field(min_length=1)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    category: str = Field(min_length=1)
    weight: Optional[str] = None
    additional_notes: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Wireless Mouse",
                "brand": "TechLogi",
                "price": 29.99,
                "stock": 150,
                "category": "Electronics",
                "weight": "120 grams",
                "additional_notes": "has bluetooth"
            }
        }
    }