from fastapi import APIRouter, Depends
from dependencies.auth import get_current_user
from firebase import db

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/")
async def list_items(user: dict = Depends(get_current_user)):
    uid   = user["uid"]
    docs  = db().collection("items").where("owner", "==", uid).stream()
    return [{"id": d.id, **d.to_dict()} for d in docs]

@router.post("/")
async def create_item(payload: dict, user: dict = Depends(get_current_user)):
    doc_ref = db().collection("items").document()
    doc_ref.set({**payload, "owner": user["uid"]})
    return {"id": doc_ref.id}