from pydantic import BaseModel, Field
from typing import Optional, List


class PlanItem(BaseModel):
    name: str
    bought: bool = False


class Plan(BaseModel):
    id: str
    name: str
    category: str
    people_involved: str
    date: str
    location_id: Optional[str] = None
    items: List[PlanItem] = []
    budget: float
    status: str
    additional_details: Optional[str] = None

class PlanRequest(BaseModel):
    name: str = Field(min_length=1)
    category: str = Field(min_length=1)
    people_involved: str = Field(min_length=1)
    date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    location_id: Optional[str] = None
    items: List[PlanItem] = []
    budget: float = Field(ge=0)
    status: str = Field(default="Pending")
    additional_details: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Barbacoa en la Sierra",
                "category": "Social",
                "people_involved": "Grupo de Universidad",
                "date": "2026-05-20",
                "location_id": "m5-sierra",
                "items": [
                    {"name": "Carne", "bought": False},
                    {"name": "Bebidas", "bought": True}
                ],
                "budget": 120.0,
                "status": "Pending",
                "additional_details": "Confirmar quién trae el coche"
            }
        }
    }
    