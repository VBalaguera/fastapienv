import json

BOOKS = [
    {"title": "Shadows of Truth", "author": "Nina Moore", "category": "history"},
    {"title": "Moral Compass", "author": "Jared Ellis", "category": "ethics"},
    {"title": "The Greater Good", "author": "Leah Winters", "category": "mathematics"},
    {"title": "Gray Decisions", "author": "Omar Lane", "category": "science"},
    {"title": "Right or Wrong", "author": "Nina Moore", "category": "history"},
    {"title": "Virtue and Vice", "author": "Daniel Cho", "category": "ethics"},
    {"title": "Beyond Duty", "author": "Harper Wells", "category": "biology"},
    {"title": "Minds of Morality", "author": "Felix Rivera", "category": "science"},
    {"title": "Justice in Shadows", "author": "Sophie Lin", "category": "sociology"}
]


def get_books_json():
    with open("data/books.json", "r") as f:
        return json.load(f)
