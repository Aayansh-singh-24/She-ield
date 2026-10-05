from fastapi import APIRouter, Depends, status, BackgroundTasks
from src.emergency.dependencies.service import EmergencyService
from src.utils.db import get_db
from src.location.schema.dtos import locationAlertSchema
from src.emergency.schema import LiveLocationSchema
from src.utils.helpers import send_emergency_email
from sqlalchemy.orm import Session
from src.user.controller import is_authenticated
from src.user.models import UserModel


router = APIRouter(prefix="/location", tags=["Location_Sharing"])

@router.post("/alert", status_code=status.HTTP_200_OK)
def alert(
    location: locationAlertSchema,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(is_authenticated),
):
    service = EmergencyService(db)

    # 1. Create new emergency session
    session = service.create_new_session(current_user)

    # 2. Save initial coordinates if provided
    if location.latitude is not None and location.longitude is not None:
        try:
            service.save_location(
                session.session_id,
                LiveLocationSchema(
                    latitude=location.latitude,
                    longitude=location.longitude,
                    speed=0.0,
                    accuracy=0.0,
                ),
                current_user,
            )
        except Exception:
            pass

    # 3. Build live tracking URL
    tracking_url = service._build_tracking_url_(session.session_id)

    # 4. Retrieve trusted contacts
    try:
        contacts = service._get_contact_(current_user)
    except Exception:
        contacts = []

    # 5. Dispatch email alerts in the background
    email_dispatched = False
    for contact in contacts:
        if getattr(contact, "email", None):
            background_tasks.add_task(
                send_emergency_email,
                contact.email,
                contact.name,
                current_user.name,
                tracking_url,
                location.message,
            )
            email_dispatched = True

    # If contacts don't have emails yet, alert the user's registered email
    if not email_dispatched and getattr(current_user, "email", None):
        background_tasks.add_task(
            send_emergency_email,
            current_user.email,
            current_user.name,
            current_user.name,
            tracking_url,
            location.message,
        )

    return {
        "message": "Emergency session started successfully.",
        "session_id": session.session_id,
        "tracking_url": tracking_url,
    }


@router.post("/stop", status_code=status.HTTP_200_OK)
def stop_alert(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(is_authenticated),
):
    service = EmergencyService(db)
    active_session = service._get_active_session_(current_user)
    if active_session:
        service.end_session(active_session.session_id, current_user)
        return {
            "message": "Emergency session ended successfully.",
            "session_id": active_session.session_id,
        }
    return {"message": "No active emergency session found."}
