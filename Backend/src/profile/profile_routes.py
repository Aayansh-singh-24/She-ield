import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user.controller import is_authenticated
from src.user.models import UserModel
from src.profile.dtos import UpdateUserSchema, UpdateUserResponseSchema

router = APIRouter(prefix="/profile", tags=["Profile"])

PROFILE_DIR = "profiles"

@router.put("/update_user_credentials", response_model=UpdateUserResponseSchema)
def update_user_credentials(
    payload: UpdateUserSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(is_authenticated)
):
    if payload.username is not None:
        username = payload.username.strip()
        if username:
            # Check if username exists
            existing = db.query(UserModel).filter(UserModel.username == username, UserModel.id != current_user.id).first()
            if existing:
                raise HTTPException(status_code=400, detail="Username already exists")
            current_user.username = username
            
    if payload.email is not None:
        email = payload.email.strip()
        if email:
            # Check if email exists
            existing = db.query(UserModel).filter(UserModel.email == email, UserModel.id != current_user.id).first()
            if existing:
                raise HTTPException(status_code=400, detail="Email already exists")
            current_user.email = email
            
    db.commit()
    db.refresh(current_user)
    return current_user

@router.post("/upload_profile", status_code=status.HTTP_200_OK)
async def upload_profile(
    file: UploadFile = File(...),
    current_user: UserModel = Depends(is_authenticated)
):
    os.makedirs(PROFILE_DIR, exist_ok=True)
    # Extract extension
    ext = file.filename.split(".")[-1] if file.filename and "." in file.filename else "png"
    # We can delete any existing profile pictures for this user to avoid conflicts
    for f in os.listdir(PROFILE_DIR):
        if f.startswith(f"{current_user.id}."):
            try:
                os.remove(os.path.join(PROFILE_DIR, f))
            except Exception:
                pass
                
    filename = f"{current_user.id}.{ext}"
    filepath = os.path.join(PROFILE_DIR, filename)
    
    with open(filepath, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
        
    return {"message": "Profile picture uploaded successfully"}

@router.get("/get_profile/{id}")
def get_profile(
    id: int,
    db: Session = Depends(get_db)
):
    # Find user profile image in PROFILE_DIR
    if not os.path.exists(PROFILE_DIR):
        raise HTTPException(status_code=404, detail="Profile picture not found")
        
    for f in os.listdir(PROFILE_DIR):
        if f.startswith(f"{id}."):
            filepath = os.path.join(PROFILE_DIR, f)
            # Determine content type based on extension
            ext = f.split(".")[-1].lower()
            media_type = f"image/{ext}" if ext in ["png", "jpg", "jpeg", "gif"] else "image/png"
            return FileResponse(filepath, media_type=media_type)
            
    raise HTTPException(status_code=404, detail="Profile picture not found")
