from http.client import HTTPException

from fastapi import Body, FastAPI, Request
from models import BookRequest, Book
from books_data import get_books_json
from uuid import uuid4

app = FastAPI()

books = get_books_json()

'''uvicorn books:app --reload to run this app
or
fastapi run books.py
fastapi dev books.py'''

'''remember: FastAPI has SWAGGER'''


@app.get('/')
async def first_api():
    return 'welcome to Satellite'


'''in this moment I am returning the dictionary from another py file'''
'''get'''


@app.get('/books')
async def books_api():
    return books


'''@app.get("/books/{book_title}")
async def read_all_books(book_title: str):
    for book in books:
        if book.get('title').casefold() == book_title.casefold():
            return book
    else:
        return 'Book not found!'
'''


'''@app.get('/books/')
async def read_category_by_query(category: str):
    books_to_return = []
    for book in books:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return'''


@app.get('/books/{book_author}/')
async def read_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in books:
        if book.get('author').casefold() == book_author.casefold() and \
                book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


@app.get("/books/{book_id}")
async def read_book_by_id(book_id: str):
    for book in books:
        if book["id"] == book_id:
            return book


@app.get('/books/')
async def read_books_by_rating(book_rating: int):
    books_to_return = []
    for book in books:
        if book.get('rating') == book_rating:
            books_to_return.append(book)
    return books_to_return


'''post'''


@app.post('/books/create_book')
async def post_book(book_req: BookRequest):
    new_book = Book(
        id=str(uuid4()),
        **book_req.dict()
    )
    books.append(new_book)
    return {"message": "Book created", "book_id": new_book.id}


def find_book_it(book: Book):
    book.id = 1 if len(books) == 0 else books[-1].id + 1
    return book


'''put'''


@app.put('/books/{book_id}/update_book')
async def put_book(book_id: str, updated_book: BookRequest):
    for i in range(len(books)):
        if books[i].get('id') == book_id:
            books[i] = updated_book


'''delete'''


@app.delete('/book/{book_id}')
async def delete_book(book_id: str):
    for i in range(len(books)):
        if books[i].get('id') == book_id:
            books.pop(i)
            break
