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
            "image":     data.get("image") or translation.get("image"),
            "date":      data.get("date") or translation.get("date"),
            "createdAt": data.get("createdAt") or translation.get("createdAt"),
            **translation,
        })
    return posts

@router.get("/{slug}")
def get_post(slug: str, lang: str = "en"):
    print(f">>> HIT: slug='{slug}' lang='{lang}'")
    try:
        docs = (
            db().collection("posts")
            .where(f"{lang}.slug", "==", slug)
            .limit(1)
            .stream()
        )
        found = list(docs)
        print(f">>> Found {len(found)} documents")
        for d in found:
            data = d.to_dict()
            translation = data.get(lang, data.get("en", {}))
            return {
                "id":        d.id,
                "image":     data.get("image") or translation.get("image"),
                "date":      data.get("date") or translation.get("date"),
                "createdAt": data.get("createdAt") or translation.get("createdAt"),
                **translation,
            }
        raise HTTPException(status_code=404, detail="Post not found")
    except HTTPException:
        raise
    except Exception as e:
        print(f">>> ERROR: {e}")
        raise HTTPException(status_code=500, detail=str(e))