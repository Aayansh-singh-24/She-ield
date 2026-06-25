from fastapi import FastAPI
from src.utils.db import Base, engine
from src.user.models import UserModel
from fastapi.middleware.cors import CORSMiddleware
from src.trusted_contact.routes import contact_route
from src.location.routes import location_route
from src.user import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SafeHer Backend")

app.include_router(contact_route.router)
app.include_router(location_route.router)
app.include_router(router.user_routes)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for testing only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "SafeHer Backend is running"}


