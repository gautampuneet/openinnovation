from fastapi import FastAPI
from src.routers import image_router
from src.database import init_db

app = FastAPI()

# Initialize the database when the app starts
init_db()

app.include_router(image_router.router)

