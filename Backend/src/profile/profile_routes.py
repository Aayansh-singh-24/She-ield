import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user.controller import is_authenticated
from src.user.models import UserModel
from src.profile.dtos import UpdateUserSchema, UpdateUserResponseSchema, UpdatePassword
from src.profile.controller import ProfileService, UserService

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.post("/upload_profile")
async def upload_profile(db:Session = Depends(get_db), file:UploadFile = File(...), current_user:UserModel = Depends(is_authenticated)):
    profile = ProfileService(db, current_user)
    return await profile.upload_profile(file)



@router.patch("/update_user_credentials", response_model=UpdateUserResponseSchema)
def update_user_credentials(body:UpdateUserSchema, db:Session = Depends(get_db), current_user:UserModel = Depends(is_authenticated)):
    user = UserService(db,current_user)
    return user.update_user_credentials(body)



@router.get("/get_profile")
def get_profile(db:Session = Depends(get_db), current_user:UserModel = Depends(is_authenticated)):
    profile = ProfileService(db,current_user)
    return profile.get_profile()



@router.put("/update_password")
def update_password(body:UpdatePassword, db:Session = Depends(get_db), current_user:UserModel = Depends(is_authenticated)):
    user = UserService(db,current_user)
    return user.update_password(body)
