from fastapi import FastAPI
from routers import books_router, places_router, products_router

app = FastAPI(title="Satellite API")

app.include_router(books_router)
app.include_router(places_router)
app.include_router(products_router)


@app.get("/")
async def root():
    return {"message": "Welcome to Satellite"}
