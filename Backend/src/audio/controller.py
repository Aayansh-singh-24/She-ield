from fastapi import HTTPException,status,UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from src.user.models import UserModel
from src.audio.model import AudioModel
from src.utils.settings import setting


import os
import uuid
import aiofiles
import mimetypes



async def storage(file:UploadFile) -> str:
    UPLOAD_DIR = setting.UPLOAD_DIR
    os.makedirs(UPLOAD_DIR,exist_ok=True)

    if file.filename is None:
        raise ValueError("Filename is missing")
    
    ext = file.filename.split(".")[-1]  # extracting of extension

    unique_id = f"{uuid.uuid4()}.{ext}" # Generating unique_id with file name -> "njkbvjdkbvhj.mp3"

    path = os.path.join(UPLOAD_DIR,unique_id) 

    # Store audio file in chunk to protect the excessive use of RAM
    async with aiofiles.open(path,"wb") as f:
        while chunk := await file.read(1024*1024):
            await f.write(chunk)

    return path



async def upload_audio(file:UploadFile, db:Session, current_user:UserModel):

    ALLOWED_TYPES = [
        "audio/mpeg",
        "audio/mp3",
        "audio/wav",
        "audio/x-wav",
        "audio/m4a",
        "audio/webm",
        "audio/webm;codecs=opus",
        "audio/ogg",
    ]

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid audio type")

    path = await storage(file)

    new_file = AudioModel(filename = file.filename, filepath = path, user_id = current_user.id)

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return {
        "id" : new_file.id,
        "filename" : new_file.filename
    }
    

    
def get_audio(id:int, db:Session, current_user:UserModel):
    audio = db.query(AudioModel).filter(
        AudioModel.user_id == current_user.id,
        AudioModel.id == id
    ).first()

    if not audio:
        raise HTTPException(status_code=404, detail="audio not found...")
    
    if not os.path.exists(audio.filepath):
        raise HTTPException(status_code=404,detail="Audio file missing from server")
    
    mime, _ = mimetypes.guess_type(audio.filepath)
    
    return FileResponse(
        path=audio.filepath,
        media_type=mime,
        filename=audio.filename,
    )


def delete_audio(id:int, db:Session, current_user:UserModel):
    audio = db.query(AudioModel).filter(
        AudioModel.user_id == current_user.id,
        AudioModel.id == id
    ).first()

    if not audio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="audio not found")
    
    # Delete file from disk...
    if os.path.exists(audio.filepath):
        os.remove(audio.filepath)


    db.delete(audio)
    db.commit()

    return None