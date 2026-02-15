from fastapi import APIRouter, Request, HTTPException, Path, Query
from models import BookRequest, Book
from uuid import uuid4
import os
import json

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

def get_books_json():
    # Assuming your JSON is in a 'data' folder like in your screenshot
    file_path = os.path.join("data", "books.json")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

books = get_books_json()

'''uvicorn books:app --reload to run this app
or
fastapi run books_router.py
fastapi dev books_router.py'''

'''remember: FastAPI has SWAGGER'''


@router.get('/')
async def first_api():
    return 'welcome to Satellite'


'''in this moment I am returning the dictionary from another py file'''
'''get'''


@router.get('/books')
async def books_api():
    return books


'''@router.get("/books/{book_title}")
async def read_all_books(book_title: str):
    for book in books:
        if book.get('title').casefold() == book_title.casefold():
            return book
    else:
        return 'Book not found!'
'''


'''@router.get('/books/')
async def read_category_by_query(category: str):
    books_to_return = []
    for book in books:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return'''


@router.get('/books/author/{book_author}/')
async def read_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in books:
        if book.get('author').casefold() == book_author.casefold() and \
                book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


@router.get("/books/id/{book_id}")
async def read_book_by_id(book_id: str = Path()):
    """ We need a path there """
    for book in books:
        if book.get("id") == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@router.get('/books/rating/')
async def read_books_by_rating(book_rating: float = Query(gt=-1, lt=11)):
    books_to_return = []
    for book in books:
        if book.get('rating') == book_rating:
            books_to_return.append(book)
    return books_to_return


@router.get('/books/published')
async def read_books_by_publish_date(published_date: int = Query(gt=0, lt=2100)):
    books_to_return = []
    for book in books:
        if book.get('published_date') == published_date:
            books_to_return.append(book)
    return books_to_return


'''post'''


@router.post('/books/create_book')
async def post_book(book_req: BookRequest):
    new_book = Book(
        id=str(uuid4()),
        **book_req.model_dump()
    )

    books.append(new_book.model_dump())
    return {"message": "Book created", "book_id": new_book.id}


def find_book_id(book: Book):
    book.id = 1 if len(books) == 0 else books[-1].get("id")
    return book


'''put'''


@router.put('/books/{book_id}/update_book')
async def put_book(book_id: str, updated_book: BookRequest):
    for i in range(len(books)):
        if books[i].get('id') == book_id:
            updated = Book(
                id=book_id,
                **updated_book.model_dump()
            )
            books[i] = updated.model_dump()
            return {"message": "Book updated"}
    raise HTTPException(status_code=404, detail="Book not found")


'''delete'''


@router.delete('/book/{book_id}')
async def delete_book(book_id: str):
    for i in range(len(books)):
        if books[i].get('id') == book_id:
            books.pop(i)
            return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")