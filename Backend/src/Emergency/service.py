from __future__ import annotations
from fastapi import HTTPException,status
import logging
from datetime import datetime, UTC
from sqlalchemy.orm import Session
from src.utils.settings import setting
from twilio.rest import Client
from src.user.models import UserModel
from src.trusted_contact.models.model import TrustedContactsModel
from src.Emergency.model import EmergencySession, LocationHistory
from src.Emergency.schema import LiveLocationSchema

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
        session = self._create_session_(current_user)
        return session
    

    def get_session(self, session_id:str):
        session = self.db.query(EmergencySession).filter(
            EmergencySession.session_id == session_id
        ).first()

        if not session:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="session not found")
        
        return session
    
    def validate_active_session(self, session_id:str):
        
        session = self.get_session(session_id)

        if session.status != "ACTIVE":

            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Emergency session is no longer active.",)

        return session
    
    def validate_user_owner(self, session_id:str, current_user:UserModel):
        
        session = self.validate_active_session(session_id)

        if current_user.id != session.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,  detail="You are not allowed to update this emergency.")
        
        return session
    
    ##############################
    # location
    #############################

    def save_location(self, session_id:str, body:LiveLocationSchema, current_user:UserModel):
        session = self.validate_user_owner(session_id, current_user)

        location = LocationHistory(
            session_id = session_id,
            latitude = body.latitude,
            longitude = body.longitude,
            speed = body.speed,
            accuracy = body.accuracy,
            timestamp = datetime.now(UTC)
        )

        try:
            self.db.add(location)
            self.db.commit()
            self.db.refresh(location)
            logger.info("Location stored for session %s", session.session_id)
        except Exception:
            self.db.rollback()
            raise

        
        return location

    def get_latest_location(self, session_id:str):

        session = self.validate_active_session(session_id)

        latest_location = self.db.query(LocationHistory).filter( 
            LocationHistory.session_id == session_id
            ).order_by(
                LocationHistory.timestamp.desc()
                ).first
        
        return latest_location

    def end_session(self, session_id:str, current_user:UserModel):

        session = self.validate_user_owner(session_id,current_user)
        session.status = "ENDED"
        session.ended_time = datetime.now(UTC)

        self.db.commit()

        logger.info("Emergency session %s ended.",session.session_id)

        return session
