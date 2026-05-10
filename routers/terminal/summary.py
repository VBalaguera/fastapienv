from fastapi import APIRouter, HTTPException
from firebase import db

router = APIRouter(prefix="/summary", tags=["summary"])

@router.get("/")
def get_summary(lang: str = "en"):
    doc = db().collection("summary").document("main").get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Summary not found")
    data = doc.to_dict()
    return data.get(lang, data.get("en"))