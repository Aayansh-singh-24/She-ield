from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.utils.db import Base, engine
from src.user.models import UserModel
from fastapi.middleware.cors import CORSMiddleware
from src.trusted_contact.routes import contact_route
from src.location.routes import location_route
from src.user import user_route
from src.audio import audio_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SafeHer Backend")

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(contact_route.router)
app.include_router(location_route.router)
app.include_router(user_route.router)
app.include_router(audio_routes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for testing only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return FileResponse("static/index.html")



