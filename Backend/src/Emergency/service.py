from __future__ import annotations
from fastapi import HTTPException,status
import logging
from datetime import datetime, UTC
from sqlalchemy.orm import Session
from src.utils.settings import setting
from twilio.rest import Client
from src.user.models import UserModel
from src.trusted_contact.models.model import TrustedContactsModel
from src.Emergency.model import EmergencySession

logger = logging.getLogger(__name__)

class EmergencyService:
    def __init__(self, db:Session):
        self.db = db
        self.client = Client(setting.TWILIO_ACCOUNT_SID, setting.TWILIO_AUTH_TOKEN)
        self.phoneNo = setting.TWILIO_PHONE_NUMBER
        self.base_tracking_url = getattr(setting, "TRACKING_URL",  "http://localhost:8000/track")


    def _get_contact_(self,current_user:UserModel):
        contact = self.db.query(TrustedContactsModel).filter(TrustedContactsModel.userId == current_user.id).all()

        if not contact:
            raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail="contact not found")
        
        return contact
    

    def _build_tracking_url_(self, session_id:str):
        return f"{self.base_tracking_url}/{session_id}"
    

    def _format_phone_number_(self, contact: TrustedContactsModel):

        country = contact.country_code or "+91"

        if not country.startswith("+"):
            country = "+" + country

        return f"{country}{contact.phoneNo}"
    


    def _tracking_message_(self, current_user: UserModel, tracking_url: str, custom_message: str):

        message = custom_message or "I need immediate help."
        return (
            "EMERGENCY ALERT\n\n"
            f"{current_user.name} needs immediate assistance.\n\n"
            f"Message:\n"
            f"{message}\n\n"
            "Track Live Location:\n"
            f"{tracking_url}"
        )
    
    # Returns the currently active emergency session  for the authenticated user.
    
    def _get_active_session_(self, current_user:UserModel):

        session = self.db.query(EmergencySession).filter(
            EmergencySession.user_id == current_user.id,
            EmergencySession.status == "ACTIVE"
        ).first()

        return session
    
    # Ends the previous emergency session.
    
    def _close_session_(self, current_user):

        active_session = self.get_active_session(current_user)

        if not active_session:
            return
        
        logger.info( "Closing previous emergency session %s for user %s", active_session.session_id, current_user.id)

        active_session.status = "ENDED"
        active_session.ended_time = datetime.now(UTC)

        self.db.commit()

    # Create a new Session. 

    def _create_session_(self, current_user:UserModel):
        session = EmergencyService(
            user_id = current_user.id,
            status = "ACTIVE"
        )

        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        logger.info("Emergency session %s created for user %s", session.session_id, current_user.id)

        return session
    
    # public function 
    def create_new_session(self, current_user):
        self.close_session(current_user)
        session = self.create_session(current_user)
        return session
