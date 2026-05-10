import json
import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

# ── Firebase init ─────────────────────────────────────────────────────────────
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

def clean_tools(tools):
    """Normalize tools array — keep only what's needed, drop empty img urls."""
    return [
        {
            "id":        t.get("id"),
            "title":     t.get("title"),
            "shortName": t.get("shortName"),
            "imgUrl":    t.get("img", {}).get("url") or None,
        }
        for t in (tools or [])
    ]

# ── Projects ──────────────────────────────────────────────────────────────────
def seed_projects():
    en_items = load_json("projects", "projects-en.json")
    es_items = load_json("projects", "projects-es.json")

    es_by_id = {p["id"]: p for p in es_items}

    batch = db.batch()

    for en in en_items:
        project_id = str(en["id"])
        es = es_by_id.get(en["id"], {})

        doc = {
            # ── Shared ─────────────────────────────────────────────────────
            "projectId": en["id"],
            "title":     en.get("title"),
            "url":       en.get("url"),
            "createdAt": en.get("createdAt"),
            "tools":     clean_tools(en.get("tools")),

            # ── English ────────────────────────────────────────────────────
            "en": {
                "description":   en.get("description"),
                "subtitledate":  en.get("subtitledate"),
                "content":       en.get("content.markdown"),
            },

            # ── Spanish ────────────────────────────────────────────────────
            "es": {
                "description":   es.get("description"),
                "subtitledate":  es.get("subtitledate"),
                "content":       es.get("content.markdown"),
            },
        }

        doc_ref = db.collection("projects").document(project_id)
        batch.set(doc_ref, doc)
        print(f"  Queued project {project_id}: {en.get('title')}")

    batch.commit()
    print(f"\n✓ Seeded {len(en_items)} bilingual projects into 'projects'\n")


# ── Work Experience ───────────────────────────────────────────────────────────
def seed_work_exp():
    en_items = load_json("work-exp", "work-exp-en.json")
    es_items = load_json("work-exp", "work-exp-es.json")

    es_by_id = {p["id"]: p for p in es_items}

    batch = db.batch()

    for en in en_items:
        work_id = str(en["id"])
        es = es_by_id.get(en["id"], {})

        doc = {
            # ── Shared ─────────────────────────────────────────────────────
            "workId":    en["id"],
            "title":     en.get("title"),
            "url":       en.get("url"),
            "createdAt": en.get("createdAt"),
            "tools":     clean_tools(en.get("tools")),

            # ── English ────────────────────────────────────────────────────
            "en": {
                "description":  en.get("description"),
                "subtitledate": en.get("subtitledate"),
            },

            # ── Spanish ────────────────────────────────────────────────────
            "es": {
                "description":  es.get("description"),
                "subtitledate": es.get("subtitledate"),
            },
        }

        doc_ref = db.collection("work_exp").document(work_id)
        batch.set(doc_ref, doc)
        print(f"  Queued work exp {work_id}: {en.get('title')}")

    batch.commit()
    print(f"✓ Seeded {len(en_items)} bilingual entries into 'work_exp'\n")


# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Seeding projects...")
    seed_projects()

    print("Seeding work experience...")
    seed_work_exp()

    print("All done!")