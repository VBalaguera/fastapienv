from fastapi import APIRouter, HTTPException
from uuid import uuid4
from models import Product, ProductRequest
import json
import os


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

def get_products_json():
    file_path = os.path.join("data", "products.json")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

products = get_products_json()

# --- PRODUCTS ENDPOINTS ---

@router.get("/products")
async def get_all_products():
    return products

@router.post("/products/create")
async def create_product(prod_req: ProductRequest):
    new_prod = Product(id=str(uuid4()), **prod_req.model_dump())
    products.append(new_prod.model_dump())
    return {"message": "Product added", "id": new_prod.id}

@router.put("/products/{product_id}")
async def update_product(product_id: str, updated_prod: ProductRequest):
    for i, prod in enumerate(products):
        if prod['id'] == product_id:
            products[i] = Product(id=product_id, **updated_prod.model_dump()).model_dump()
            return {"message": "Product updated"}
    raise HTTPException(status_code=404, detail="Product not found")