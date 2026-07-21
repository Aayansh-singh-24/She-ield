from fastapi import HTTPException,status,BackgroundTasks
from sqlalchemy.orm import Session

from src.location.schema.dtos import locationAlertSchema

from src.user.models import UserModel
from src.emergency.dependencies.service import EmergencyService


def send_sms(service:EmergencyService, phone_no:str,message:str):
    service.client.messages.create(
        body=message,
        from_=service.phoneNo,
        to=phone_no,\
    )

def alert(location:locationAlertSchema, background_tak:BackgroundTasks, db:Session, current_user:UserModel):


    service = EmergencyService(db)

    # create new emergency session
    session = service.create_new_session(current_user)

    # tracking url
    tracking_url = service.create_new_session(current_user)

    contacts = service._get_contact_(current_user)

    message = service._tracking_message_(current_user,tracking_url, location.message)

    for contact in contacts:
        phone_no = service._format_phone_number_(contact)

        background_tak(send_sms, service, phone_no, message)

    return {
        "message": "Emergency session started successfully.",
        "session_id": session.session_id,
        "tracking_url": tracking_url,
    }