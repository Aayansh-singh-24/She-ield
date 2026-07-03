from fastapi import status, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from src.user.models import UserModel
from src.profile.model import ProfileModel
from src.utils.settings import setting


import os,uuid,mimetypes
import aiofiles
from typing import cast

async def storage(file:UploadFile):
    UPLOAD_PROFILE_DIR = setting.PROFILE_DIR
    os.makedirs(UPLOAD_PROFILE_DIR, exist_ok=True)

    if file.filename is None:
        raise ValueError("Filename is missing")
    
    extension = file.filename.split(".")[-1]
    unique_id = f"{uuid.uuid4()}.{extension}"

    path = os.path.join(UPLOAD_PROFILE_DIR,unique_id)

    # store profile picture in s3 storage
    async with aiofiles.open(path,"wb") as f:
        while chunks := await file.read(1024*1024):
            await f.write(chunks)

    return path

async def upload_profile(db:Session, file:UploadFile, current_user:UserModel):
        
    ALLOWED_IMAGE_TYPES = [
        "image/jpeg",   
        "image/png",    
        "image/webp",   
    ]

    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="image type is not valid..")
    
    path = await storage(file)

    existing_profile = db.query(ProfileModel).filter(
        ProfileModel.user_id == current_user.id
    ).first()


    if existing_profile:
        if os.path.exists(existing_profile.filepath):
            os.remove(existing_profile.filepath)

        if file.filename is None:
            raise HTTPException(status_code=400,detail="Filename is missing")

        existing_profile.filename = cast(str,file.filename)
        existing_profile.filepath = path

        db.commit()
        db.refresh(existing_profile)

        return {
            "id" : existing_profile.id,
            "filename" : existing_profile.filename
        }
        

    new_profile = ProfileModel(filename=file.filename, filepath=path, user_id=current_user.id)

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return {"id" : new_profile.id, "filename" : new_profile.filename}



def get_profile(id:int, db:Session, current_user:UserModel):
    profile = db.query(ProfileModel).filter(
        ProfileModel.user_id == current_user.id,
        ProfileModel.id == id
    ).first()

    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="profile not found")
    
    if not os.path.exists(profile.filepath):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="profile path not found")
    
    typeOfImage,_ = mimetypes.guess_type(profile.filepath)


    return FileResponse(
        path=profile.filepath,
        media_type=typeOfImage,
        filename=profile.filename
    )

def delete_profile(id:int, db:Session, current_user:UserModel):
    profile = db.query(ProfileModel).filter(
        ProfileModel.user_id == current_user.id,
        ProfileModel.id == id
    ).first()

    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="profile not found")
    
    if os.path.exists(profile.filepath):
        os.remove(profile.filepath)

    db.delete(profile)
    db.commit()

    return None

