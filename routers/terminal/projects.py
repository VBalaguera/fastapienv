from fastapi import APIRouter, HTTPException
from firebase import db

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("/")
def get_projects(lang: str = "en"):
    docs = (
        db().collection("projects")
        .order_by("createdAt", direction="DESCENDING")
        .stream()
    )
    projects = []
    for d in docs:
        data = d.to_dict()
        translation = data.get(lang, data.get("en", {}))
        projects.append({
            "id":        d.id,
            "title":     data.get("title"),
            "url":       data.get("url"),
            "tools":     data.get("tools"),
            "createdAt": data.get("createdAt"),
            **translation,
        })
    return projects