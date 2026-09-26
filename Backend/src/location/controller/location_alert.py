from fastapi import HTTPException,status,BackgroundTasks
from sqlalchemy.orm import Session

from src.location.schema.dtos import locationAlertSchema

from src.user.models import UserModel
from src.emergency.dependencies.service import EmergencyService
from twilio.base.exceptions import TwilioRestException

import logging

logger = logging.getLogger(__name__)


def send_sms(service:EmergencyService, phone_no:str,message:str):
    try:
        service.client.messages.create(
            body=message,
            from_=service.phoneNo,
            to=phone_no
        )

        logger.info("Emergency SMS sent successfully to %s", phone_no)
    except TwilioRestException as exc:
        logger.error(
            "Failed to send emergency SMS to %s: %s",
            phone_no,
            exc
        )

def alert(location:locationAlertSchema, background_tak:BackgroundTasks, db:Session, current_user:UserModel):


    service = EmergencyService(db)

    # create new emergency session
    session = service.create_new_session(current_user)

    # tracking url
    tracking_url = service._build_tracking_url_(session.session_id)

    contacts = service._get_contact_(current_user)

    message = service._tracking_message_(current_user,tracking_url, location.message)

    for contact in contacts:
        phone_no = service._format_phone_number_(contact)

        background_tak.add_task(send_sms, service, phone_no, message)

    return {
        "message": "Emergency session started successfully.",
        "session_id": session.session_id,
        "tracking_url": tracking_url,
    }