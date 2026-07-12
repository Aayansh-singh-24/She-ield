from fastapi import status, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from src.user.models import UserModel
from src.profile.models import ProfileModel
from src.utils.settings import setting
from src.profile.dtos import UpdateUserSchema
from src.profile.dtos import UpdatePassword
from src.user.controller import get_password_hash, verify_password

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
        
    if not file.content_type or not file.content_type.startswith("image/"):
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



def get_profile(db:Session, current_user:UserModel):

    profile = db.query(ProfileModel).filter(
        ProfileModel.user_id == current_user.id,
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


def update_user_credentials(body:UpdateUserSchema, db:Session, current_user:UserModel):

    data = body.model_dump(exclude_unset=True) # the data which are not present in body will not assigned None automatically

    if "email" in data:
        existing_email_user = db.query(UserModel).filter(
            UserModel.email == data["email"]
        ).first()

        if existing_email_user and existing_email_user.id != current_user.id:
           raise HTTPException(400, "Email  already exists")
        
        current_user.email = data["email"]

    if "username" in data:
        existing_username_user = db.query(UserModel).filter(
            UserModel.username == data["username"]
        ).first()

        if existing_username_user and existing_username_user.id != current_user.id:
            raise HTTPException(400, "Phone number already exists")
        
        current_user.username = data["username"]

    db.commit()
    db.refresh(current_user)

    return current_user


def update_password(body:UpdatePassword, db:Session, current_user:UserModel):

    data = body.model_dump()


    if not verify_password(data["current_password"], current_user.hash_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current Password is incorrect")
    
    if verify_password(data["new_password"], current_user.hash_password):
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="New password cannot be the same as the current password.")
    

    if data["new_password"] != data["confirm_password"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password not matched")
    
    try:
        current_user.hash_password = get_password_hash(data["new_password"])

        db.commit()
        db.refresh(current_user)
    except Exception:
        db.rollback()
        raise

    return None

