from fastapi import status, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from src.user.models import UserModel
from src.profile.models import ProfileModel
from src.utils.settings import setting
from src.profile.dtos import UpdateUserSchema
from src.profile.dtos import UpdatePassword,UpdateUserResponseSchema
from src.user.controller import get_password_hash, verify_password

import os,uuid,mimetypes
import aiofiles
from typing import cast

class Storage:
    def __init__(self):
        self.upload_dir = setting.PROFILE_DIR
        os.makedirs(self.upload_dir,exist_ok=True)

    async def save(self,file:UploadFile) -> str:
        if file.filename is None:
            raise ValueError("Filename is missing")

        extension = file.filename.split('.')[-1]
        unique_id = f"{uuid.uuid4()}.{extension}"

        path = os.path.join(self.upload_dir, unique_id)

        # store profile picture in s3 storage
        async with aiofiles.open(path,"wb") as f:
            while chunks := await file.read(1024*1024):
                await f.write(chunks)

        return path


    def delete(self, path:str) -> None:
        if os.path.exists(path):
            os.remove(path)



class ProfileService:
    def __init__(self, db:Session, current_user:UserModel):
        self.storage = Storage()
        self.db:Session = db
        self.current_user = current_user

    @staticmethod
    def _validate_image(file: UploadFile):

        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid image type")

    async def upload_profile(self,file:UploadFile):

        self._validate_image(file)

        existing_profile = self.db.query(ProfileModel).filter(
            ProfileModel.user_id == self.current_user.id
        ).first()

        if existing_profile:
            old_path = existing_profile.filepath
            self.storage.delete(old_path)

            path = await self.storage.save(file)

            if not file.filename:
                raise ValueError("filename is missing")

            existing_profile.filename = file.filename
            existing_profile.filepath = path

            self.db.commit()
            self.db.refresh(existing_profile)

            return{"id" : existing_profile.id, "filename" : existing_profile.filename}

        new_profile = ProfileModel(
            filename = file.filename,
            filepath = path,
            user_id = self.current_user.id
        )
        try:
            self.db.add(new_profile)
            self.db.commit()
            self.db.refresh(new_profile)
        except Exception:
            self.db.rollback()
            raise

        return {"id" : new_profile.id, "filename" : new_profile.filename}


    def get_profile(self):
        profile = self.db.query(ProfileModel).filter(
            ProfileModel.user_id == self.current_user.id
        ).first()


        if not profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")


        if not os.path.exists(profile.filepath):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="profile path not exist")

        typeOfImage,_ = mimetypes.guess_type(profile.filepath)


        return FileResponse(
            path=profile.filepath,
            media_type=typeOfImage,
            filename=profile.filename
        )



class UserService:
    def __init__(self, db:Session, current_user:UserModel):
        self.db = db
        self.current_user = current_user

    def update_user_credentials(self,body: UpdateUserSchema) -> UpdateUserResponseSchema:

        data = body.model_dump(exclude_unset=True)

        if "email" in data:

            existing_user = self.db.query(UserModel).filter(
                    UserModel.email == data["email"]
                ).first()

            if existing_user and existing_user.id != self.current_user.id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already exists")

            self.current_user.email = data["email"]

        if "username" in data:

            existing_user = self.db.query(UserModel).filter(
                    UserModel.username == data["username"]
                ).first()

            if existing_user and existing_user.id != self.current_user.id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Username already exists")

            self.current_user.username = data["username"]

        try:
            self.db.commit()
            self.db.refresh(self.current_user)

        except Exception:
            self.db.rollback()
            raise

        return self.current_user


    def update_password(self,body:UpdatePassword)-> None:
        data = body.model_dump()
           
           
        if not verify_password(data["current_password"], self.current_user.hash_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current Password is incorrect")
               
        if verify_password(data["new_password"], self.current_user.hash_password):
            raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="New password cannot be the same as the current password.")
               
           
        if data["new_password"] != data["confirm_password"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password not matched")
               
        try:
                self.current_user.hash_password = get_password_hash(data["new_password"])
           
                self.db.commit()
                self.db.refresh(self.current_user)
        except Exception:
                self.db.rollback()
                raise
           
        return None





# async def storage(file:UploadFile):
#     UPLOAD_PROFILE_DIR = setting.PROFILE_DIR
#     os.makedirs(UPLOAD_PROFILE_DIR, exist_ok=True)

#     if file.filename is None:
#         raise ValueError("Filename is missing")
    
#     extension = file.filename.split(".")[-1]
#     unique_id = f"{uuid.uuid4()}.{extension}"

#     path = os.path.join(UPLOAD_PROFILE_DIR,unique_id)

#     # store profile picture in s3 storage
#     async with aiofiles.open(path,"wb") as f:
#         while chunks := await file.read(1024*1024):
#             await f.write(chunks)

#     return path



# async def upload_profile(db:Session, file:UploadFile, current_user:UserModel):
        
#     if not file.content_type or not file.content_type.startswith("image/"):
#         raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="image type is not valid..")

#     storage = Storage()
    
#     path = await storage.save(file)

#     existing_profile = db.query(ProfileModel).filter(
#         ProfileModel.user_id == current_user.id
#     ).first()


#     if existing_profile:
#         old_path = existing_profile.filepath
#         storage.delete(old_path)

#         if file.filename is None:
#             raise HTTPException(status_code=400,detail="Filename is missing")

#         existing_profile.filename = cast(str,file.filename)
#         existing_profile.filepath = path



#         db.commit()
#         db.refresh(existing_profile)


#         return {
#             "id" : existing_profile.id,
#             "filename" : existing_profile.filename
#         }
        

#     new_profile = ProfileModel(filename=file.filename, filepath=path, user_id=current_user.id)

#     db.add(new_profile)
#     db.commit()
#     db.refresh(new_profile)


#     return {"id" : new_profile.id, "filename" : new_profile.filename}



# def get_profile(db:Session, current_user:UserModel):

#     profile = db.query(ProfileModel).filter(
#         ProfileModel.user_id == current_user.id,
#     ).first()


#     if not profile:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="profile not found")
    
#     if not os.path.exists(profile.filepath):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="profile path not found")
    
#     typeOfImage,_ = mimetypes.guess_type(profile.filepath)


#     return FileResponse(
#         path=profile.filepath,
#         media_type=typeOfImage,
#         filename=profile.filename
#     )

# def delete_profile(id:int, db:Session, current_user:UserModel):
#     profile = db.query(ProfileModel).filter(
#         ProfileModel.user_id == current_user.id,
#         ProfileModel.id == id
#     ).first()

#     if not profile:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="profile not found")
    
#     if os.path.exists(profile.filepath):
#         os.remove(profile.filepath)

#     db.delete(profile)
#     db.commit()

#     return None


# def update_user_credentials(body:UpdateUserSchema, db:Session, current_user:UserModel):

#     data = body.model_dump(exclude_unset=True) # the data which are not present in body will not assigned None automatically

#     if "email" in data:
#         existing_email_user = db.query(UserModel).filter(
#             UserModel.email == data["email"]
#         ).first()

#         if existing_email_user and existing_email_user.id != current_user.id:
#            raise HTTPException(400, "Email  already exists")
        
#         current_user.email = data["email"]

#     if "username" in data:
#         existing_username_user = db.query(UserModel).filter(
#             UserModel.username == data["username"]
#         ).first()

#         if existing_username_user and existing_username_user.id != current_user.id:
#             raise HTTPException(400, "Phone number already exists")
        
#         current_user.username = data["username"]

#     db.commit()
#     db.refresh(current_user)

#     return current_user


# def update_password(body:UpdatePassword, db:Session, current_user:UserModel):

#     data = body.model_dump()


#     if not verify_password(data["current_password"], current_user.hash_password):
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current Password is incorrect")
    
#     if verify_password(data["new_password"], current_user.hash_password):
#         raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="New password cannot be the same as the current password.")
    

#     if data["new_password"] != data["confirm_password"]:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password not matched")
    
#     try:
#         current_user.hash_password = get_password_hash(data["new_password"])

#         db.commit()
#         db.refresh(current_user)
#     except Exception:
#         db.rollback()
#         raise

#     return None

