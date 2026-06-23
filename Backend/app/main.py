from fastapi import FastAPI
from app.utils.database import Base, engine
from app.models.user import User
# from app.models.trsuted_contact import alert

from app.routes import trusted_contacts,location_alert
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

app = FastAPI(title="SafeHer Backend")

app.include_router(trusted_contacts.router)
app.include_router(location_alert.router)
# app.include_router(alert.router)


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