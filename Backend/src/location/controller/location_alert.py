from fastapi import HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
import logging

from src.location.schema.dtos import locationAlertSchema
from src.user.models import UserModel
from src.emergency.dependencies.service import EmergencyService
from src.emergency.schema import LiveLocationSchema
from src.utils.helpers import send_emergency_alert_email

logger = logging.getLogger(__name__)


def alert(location: locationAlertSchema, background_tasks: BackgroundTasks, db: Session, current_user: UserModel):
    service = EmergencyService(db)

    # 1. Create or reset emergency session
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
        except Exception as exc:
            logger.warning("Failed to save initial location: %s", exc)

    # 3. Build live tracking URL
    tracking_url = service._build_tracking_url_(session.session_id)

    # 4. Fetch trusted contacts
    try:
        contacts = service._get_contact_(current_user)
    except HTTPException:
        contacts = []

    # 5. Dispatch emergency email to trusted contacts
    email_dispatched = False
    for contact in contacts:
        contact_email = getattr(contact, "email", None)
        if contact_email:
            background_tasks.add_task(
                send_emergency_alert_email,
                contact_email,
                contact.name,
                current_user.name,
                tracking_url,
                location.message,
            )
            email_dispatched = True

    # Fallback to user's registered email if no trusted contact email exists
    if not email_dispatched and getattr(current_user, "email", None):
        background_tasks.add_task(
            send_emergency_alert_email,
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