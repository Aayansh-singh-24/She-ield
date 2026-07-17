from fastapi import FastAPI
from src.utils.db import Base, engine
from src.user.models import UserModel
from fastapi.middleware.cors import CORSMiddleware
from src.trusted_contact.routes import contact_route
from src.location.routes import location_route
from src.user import user_route
from src.audio import audio_routes
from src.profile import profile_routes
from src.utils.settings import setting

Base.metadata.create_all(bind=engine)

# from sqlalchemy import inspect

app = FastAPI(title="SafeHer Backend")

app.include_router(contact_route.router)
app.include_router(location_route.router)
app.include_router(user_route.router)
app.include_router(audio_routes.router)
app.include_router(profile_routes.router)

import http
from fastapi import UploadFile, File, HTTPException

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for testing only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/detect-distress")
async def detect_distress(file: UploadFile = File(...)):
    async with http.AsyncClient(timeout=30.0) as client:
        try:
            content = await file.read()
            files = {'file': (file.filename, content, file.content_type)}
            response = await client.post("http://127.0.0.1:8001/detect-distress", files=files)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.text)
            return response.json()
        except http.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"ML Service is offline: {exc}")

@app.get("/")
def home():
    return {"message": "SafeHer Backend API is running. Access API documentation at /docs"}



