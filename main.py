from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import books_router, places_router, products_router, plans_router

app = FastAPI(title="Satellite API")

# Add this block!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, you'll change this to your React URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books_router)
app.include_router(places_router)
app.include_router(products_router)
app.include_router(plans_router)


@app.get("/")
async def root():
    return {"message": "Welcome to Satellite"}
