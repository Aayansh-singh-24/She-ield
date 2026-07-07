from fastapi import HTTPException, status, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from src.user.models import UserModel
from src.audio.model import AudioModel
from src.utils.settings import setting

import os
import uuid
import aiofiles
import mimetypes

async def storage(file: UploadFile) -> str:
    UPLOAD_DIR = setting.UPLOAD_DIR
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    if file.filename is None:
        raise ValueError("Filename is missing")
    
    ext = file.filename.split(".")[-1]  # extracting of extension

    unique_id = f"{uuid.uuid4()}.{ext}" # Generating unique_id with file name
    path = os.path.join(UPLOAD_DIR, unique_id) 

    # Store audio file in chunk to protect the excessive use of RAM
    async with aiofiles.open(path, "wb") as f:
        while chunk := await file.read(1024 * 1024):
            await f.write(chunk)

    return path

async def audio(file: UploadFile, db: Session, current_user: UserModel):
    ALLOWED_TYPES = [
        "audio/mpeg",
        "audio/mp3",
        "audio/wav",
        "audio/x-wav",
        "audio/m4a",
        "audio/webm",
        "video/webm",
        "audio/ogg",
        "application/octet-stream",
    ]

    # Quick normalize if content type is empty
    content_type = file.content_type or ""

    if content_type not in ALLOWED_TYPES and not content_type.startswith("audio/"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid audio type")

    path = await storage(file)

    new_file = AudioModel(filename=file.filename, filepath=path, user_id=current_user.id)

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return {
        "id": new_file.id,
        "name": new_file.filename
    }

def get_all_audios(db: Session, current_user: UserModel):
    audios = db.query(AudioModel).filter(AudioModel.user_id == current_user.id).all()
    return [{"id": a.id, "name": a.filename} for a in audios]

def get_audio_by_id(id: int, db: Session, current_user: UserModel):
    audio_rec = db.query(AudioModel).filter(AudioModel.id == id, AudioModel.user_id == current_user.id).first()
    if not audio_rec:
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    if not os.path.exists(audio_rec.filepath):
        raise HTTPException(status_code=404, detail="Audio file physical content not found")
        
    # Determine media type
    ext = audio_rec.filename.split(".")[-1].lower() if "." in audio_rec.filename else "webm"
    media_type = f"audio/{ext}" if ext in ["mpeg", "mp3", "wav", "webm", "ogg"] else "audio/webm"
    return FileResponse(audio_rec.filepath, media_type=media_type)

def delete_audio(id: int, db: Session, current_user: UserModel):
    audio_rec = db.query(AudioModel).filter(AudioModel.id == id, AudioModel.user_id == current_user.id).first()
    if not audio_rec:
        raise HTTPException(status_code=404, detail="Audio file not found")
        
    # Try to delete the physical file
    if os.path.exists(audio_rec.filepath):
        try:
            os.remove(audio_rec.filepath)
        except Exception:
            pass
            
    db.delete(audio_rec)
    db.commit()
    return {"message": "Audio file deleted successfully"}
