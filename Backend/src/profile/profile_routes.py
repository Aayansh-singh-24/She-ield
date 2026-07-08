import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user.controller import is_authenticated
from src.user.models import UserModel
from src.profile.dtos import UpdateUserSchema, UpdateUserResponseSchema
from src.profile import controller as service

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.post("/upload_profile")
async def upload_profile(db:Session = Depends(get_db), file:UploadFile = File(...), current_user:UserModel = Depends(is_authenticated)):
    return await service.upload_profile(db, file, current_user)


@router.patch("/update_user_credentials", response_model=UpdateUserResponseSchema)
def update_user_credentials(body:UpdateUserSchema, db:Session = Depends(get_db), current_user:UserModel = Depends(is_authenticated)):
    return service.update_user_credentials(body, db, current_user)

   
@router.get("/get_profile")
def get_profile(db:Session = Depends(get_db), current_user:UserModel = Depends(is_authenticated)):
    return service.get_profile(db, current_user)
