from fastapi import APIRouter,UploadFile,File,Depends,status
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user.controller import is_authenticated
from src.user.models import UserModel
from src.audio import controller


router = APIRouter(prefix="/recording")

@router.post("/audio",status_code=status.HTTP_201_CREATED)
async def audio(file:UploadFile = File(...), db:Session = Depends(get_db), current_user:UserModel = Depends(is_authenticated)):
    return await controller.audio(file,db,current_user)