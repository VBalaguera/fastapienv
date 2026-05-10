from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import books_router, places_router, products_router, plans_router, on_this_day_router
from routers.terminal.posts     import router as posts_router
from routers.terminal.projects  import router as projects_router
from routers.terminal.work_exp  import router as work_exp_router
from routers.terminal.summary import router as summary_router
from firebase import init_firebase

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_firebase()        # Firebase starts up once, cleanly
    yield

app = FastAPI(title="Satellite API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://swissblade.vercel.app",
        "http://localhost:3000",
        "http://localhost:5173",   # add if you use Vite locally
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Existing routers
app.include_router(books_router)
app.include_router(places_router)
app.include_router(products_router)
app.include_router(plans_router)
app.include_router(on_this_day_router)

# Future Firebase-protected routers go here, same pattern:
# from app.routers import items
# app.include_router(items.router)

# terminal implementation routers
app.include_router(posts_router)
app.include_router(projects_router)
app.include_router(work_exp_router)
app.include_router(summary_router)

@app.get("/")
async def root():
    return {"message": "Welcome to Satellite"}

@app.get("/routes")
def list_routes():
    routes = []
    for route in app.routes:
        if hasattr(route, "endpoint"):
            routes.append({
                "path":    route.path,
                "name":    route.name,
                "methods": list(route.methods) if route.methods else [],
            })
    return routes