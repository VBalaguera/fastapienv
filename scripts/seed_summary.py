import json
import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

# ── Firebase init ─────────────────────────────────────────────────────────────
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

def seed_summary():
    en = load_json("summary", "summary-en.json")
    es = load_json("summary", "summary-es.json")

    doc = {
        # ── English ────────────────────────────────────────────────────────
        "en": {
            "summary": en.get("summary"),
        },
        # ── Spanish ───────────────────────────────────────────────────────
        "es": {
            "summary": es.get("summary"),
        },
    }

    # Single document with a fixed ID — easy to fetch, easy to update
    db.collection("summary").document("main").set(doc)
    print("✓ Seeded summary document into 'summary'")

if __name__ == "__main__":
    seed_summary()