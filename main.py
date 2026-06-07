from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database.session import get_db
from routers import admin as admin_routes
from routers import animal as animal_routes
from routers import adoption_request as adoption_request_routes
from routers import animal_photos as animal_photos_routes
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="Fundación Huellitas Callejeras API",
    description="Backend para la página de adopciones de la fundación",
    version="1.0.0",
)

# CORS
origins = [
    os.getenv("FRONTEND_URL"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers
app.include_router(admin_routes.router_admin)
app.include_router(animal_routes.router_animal)
app.include_router(adoption_request_routes.router_adoptionrequest)
app.include_router(animal_photos_routes.router_photos)

@app.get("/")
def root():
    return {"message": "API Fundación Rescate Animal - OK"}


@app.get("/health")
def health():
    return {"status": "ok"}