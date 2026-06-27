from fastapi import APIRouter, Depends, status, BackgroundTasks
from src.utils.db import get_db
from src.location.schema.dtos import locationAlertSchema
from src.location.controller import location_alert
from sqlalchemy.orm import Session
from src.user.controller import is_authenticated
from src.user.models import UserModel


router = APIRouter(prefix="/location",tags=["Location_Sharing"])

@router.post("/alert",status_code=status.HTTP_200_OK)
def alert(
    location: locationAlertSchema,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(is_authenticated)
):
    return location_alert.alert(location, background_tasks, db, current_user)