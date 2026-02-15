from pydantic import BaseModel, Field
from typing import Optional

# --- PLACES MODELS ---
class Place(BaseModel):
    id: str
    name: str
    address: str
    city: str
    latitude: float
    longitude: float
    rating: float
    phone: Optional[str]
    email: Optional[str]
    website: Optional[str]
    category: str

class PlaceRequest(BaseModel):
    name: str = Field(min_length=1)
    address: str = Field(min_length=1)
    city: str = Field(min_length=1)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    rating: float = Field(ge=0, le=5)
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    category: str = Field(min_length=1)

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Puerta del Sol",
                "address": "Plaza de la Puerta del Sol",
                "city": "Madrid",
                "latitude": 40.4167,
                "longitude": -3.7038,
                "rating": 4.7,
                "phone": "+34 915 29 82 10",
                "email": "turismo@madrid.es",
                "website": "https://www.esmadrid.com",
                "category": "Landmark"
            }
        }
    }
