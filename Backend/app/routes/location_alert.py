from fastapi import APIRouter, Depends, status
from app.utils.database import get_db
from app.schemas.location_alert import locationAlertSchema
from app.controller import location_alert
from sqlalchemy.orm import Session


router = APIRouter(prefix="/location",tags=["Location_Sharing"])

# Later replace with authorize user
def get_current_user():
    return 1 

@router.post("/alert",status_code=status.HTTP_200_OK)
def alert(location:locationAlertSchema,db:Session = Depends(get_db),user=Depends(get_current_user)):
    return location_alert.alert(location, db, user)