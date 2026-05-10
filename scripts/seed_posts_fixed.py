import json
import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

if not firebase_admin._apps:
    cred = credentials.Certificate({
        "type":           "service_account",
        "project_id":     os.getenv("FIREBASE_PROJECT_ID"),
        "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
        "private_key":    os.getenv("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n"),
        "client_email":   os.getenv("FIREBASE_CLIENT_EMAIL"),
        "token_uri":      "https://oauth2.googleapis.com/token",
    })
    firebase_admin.initialize_app(cred)

db = firestore.client()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_json(subfolder, filename):
    path = os.path.join(SCRIPT_DIR, "data", subfolder, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def seed_posts():
    en_posts = load_json("blog", "posts_en.json")
    es_posts = load_json("blog", "posts_es.json")

    es_by_id = {p["id"]: p for p in es_posts}

    batch = db.batch()

    for en in en_posts:
        post_id = str(en["id"])
        es = es_by_id.get(en["id"], {})

        doc = {
            # ── Shared — always at top level ───────────────────────────────
            "postId":    en["id"],
            "image":     en.get("image"),
            "createdAt": en.get("createdAt"),
            "date":      en.get("date"),

            # ── English ────────────────────────────────────────────────────
            "en": {
                "title":      en.get("title"),
                "slug":       en.get("slug"),
                "excerpt":    en.get("excerpt"),
                "content":    en.get("content.markdown"),
                "tags":       [t["name"] for t in en.get("tags") or []],
                "categories": [c["slug"] for c in en.get("categories") or []],
            },

            # ── Spanish ────────────────────────────────────────────────────
            "es": {
                "title":      es.get("title"),
                "slug":       es.get("slug"),
                "excerpt":    es.get("excerpt"),
                "content":    es.get("content.markdown"),
                "tags":       [t["name"] for t in es.get("tags") or []],
                "categories": [c["slug"] for c in es.get("categories") or []],
            },
        }

        doc_ref = db.collection("posts").document(post_id)
        batch.set(doc_ref, doc)
        print(f"  Queued post {post_id}: {en.get('title')}")

    batch.commit()
    print(f"\n✓ Re-seeded {len(en_posts)} posts with consistent structure\n")

if __name__ == "__main__":
    seed_posts()