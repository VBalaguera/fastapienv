from fastapi import APIRouter, HTTPException
from firebase import db

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/")
def get_posts(lang: str = "en"):
    docs = (
        db().collection("posts")
        .order_by("date", direction="DESCENDING")
        .stream()
    )
    posts = []
    for d in docs:
        data = d.to_dict()
        translation = data.get(lang, data.get("en", {}))
        posts.append({
            "id":        d.id,
            "image":     data.get("image"),
            "date":      data.get("date"),
            "createdAt": data.get("createdAt"),
            **translation,
        })
    return posts

@router.get("/{slug}")
def get_post(slug: str, lang: str = "en"):
    docs = (
        db().collection("posts")
        .where(f"{lang}.slug", "==", slug)
        .limit(1)
        .stream()
    )
    for d in docs:
        data = d.to_dict()
        translation = data.get(lang, data.get("en", {}))
        return {
            "id":        d.id,
            "image":     data.get("image"),
            "date":      data.get("date"),
            "createdAt": data.get("createdAt"),
            **translation,
        }
    raise HTTPException(status_code=404, detail="Post not found")