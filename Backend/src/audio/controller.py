from fastapi import HTTPException,status,UploadFile
from sqlalchemy.orm import Session
from src.user.models import UserModel
from src.audio.model import AudioModel
from src.utils.settings import setting


import os
import uuid
import aiofiles



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



async def audio(file:UploadFile, db:Session, current_user:UserModel):

    ALLOWED_TYPES = [
        "audio/mpeg",
        "audio/mp3",
        "audio/wav",
        "audio/x-wav",
        "audio/m4a",
    ]

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid audio type")

    path = await storage(file)

    new_file = AudioModel(filename = file.filename, filepath = path, user_id = current_user.id)

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return {"message" : "audio save sucessfully"}
    

    
