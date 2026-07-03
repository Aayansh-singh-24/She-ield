from fastapi import APIRouter, status, UploadFile, File, Depends
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user.controller import is_authenticated
from src.user.models import UserModel
from src.profile import controller

router = APIRouter(prefix="/profile")

@router.post("/upload_profile")
async def upload_profile(db:Session = Depends(get_db), file:UploadFile = File(...), current_user:UserModel = Depends(is_authenticated)):
    return await controller.upload_profile(db,file,current_user)

@router.get("/get_profile/{id}")
def get_profile(id:int, db:Session = Depends(get_db), current_user:UserModel = Depends(is_authenticated)):
    return controller.get_profile(id, db, current_user)

@router.delete("/delete_profile/{id}")
def delete_profile(id:int, db:Session = Depends(get_db), current_user:UserModel = Depends(is_authenticated)):
    return controller.delete_profile(id, db, current_user)