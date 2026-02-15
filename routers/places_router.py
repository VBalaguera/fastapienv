from fastapi import APIRouter, Path, Query
from uuid import uuid4
from models import Place, PlaceRequest, Product, ProductRequest
import json
import os

router = APIRouter(
    prefix="/places",
    tags=["Places"]
)

def get_places_json():
    # Assuming your JSON is in a 'data' folder like in your screenshot
    file_path = os.path.join("data", "places.json")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

places = get_places_json()

# --- PLACES ENDPOINTS ---

@router.get("/places")
async def get_all_places():
    return places

@router.post("/places/create")
async def create_place(place_req: PlaceRequest):
    new_place = Place(id=str(uuid4()), **place_req.model_dump())
    places.append(new_place.model_dump())
    return {"message": "Place added", "id": new_place.id}

@router.get("/places/search")
async def find_place_by_city(city: str = Query(min_length=1)):
    return [p for p in places if p['city'].lower() == city.lower()]