from fastapi import APIRouter,UploadFile,File,Depends,status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user.controller import is_authenticated
from src.user.models import UserModel
from src.audio import controller


router = APIRouter(prefix="/recording")

@router.post("/upload_audio",status_code=status.HTTP_201_CREATED)
async def upload_audio(file:UploadFile = File(...), db:Session = Depends(get_db), current_user:UserModel = Depends(is_authenticated)):
    return await controller.upload_audio(file,db,current_user)


@router.get("/get_audio/{id}",status_code=status.HTTP_200_OK)
def get_audio(id:int, db:Session = Depends(get_db), current_user:UserModel = Depends(is_authenticated)):
    return controller.get_audio(id,db,current_user)

@router.delete("/audio_delete/{id}",status_code=status.HTTP_204_NO_CONTENT)
def audio_delete(id:int, db:Session=Depends(get_db),current_user:UserModel = Depends(is_authenticated)):
    return controller.delete_audio(id,db,current_user)