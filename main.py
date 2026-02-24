from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import books_router, places_router, products_router, plans_router, on_this_day_router

app = FastAPI(title="Satellite API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://swissblade.vercel.app",
                   "http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books_router)
app.include_router(places_router)
app.include_router(products_router)
app.include_router(plans_router)
app.include_router(on_this_day_router)


@app.get("/")
async def root():
    return {"message": "Welcome to Satellite"}


@app.get("/routes")
def list_routes():
    routes = []

    for route in app.routes:
        if hasattr(route, "endpoint"):
            routes.append({
                "path": route.path,
                "name": route.name,
                "methods": list(route.methods) if route.methods else []
            })

    return routes
