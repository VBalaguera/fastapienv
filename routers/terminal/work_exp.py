from fastapi import APIRouter
from firebase import db

router = APIRouter(prefix="/work-exp", tags=["work-exp"])

@router.get("/")
def get_work_exp(lang: str = "en"):
    docs = (
        db().collection("work_exp")
        .order_by("createdAt", direction="DESCENDING")
        .stream()
    )
    results = []
    for d in docs:
        data = d.to_dict()
        translation = data.get(lang, data.get("en", {}))
        results.append({
            "id":        d.id,
            "title":     data.get("title"),
            "url":       data.get("url"),
            "tools":     data.get("tools"),
            "createdAt": data.get("createdAt"),
            **translation,
        })
    return results