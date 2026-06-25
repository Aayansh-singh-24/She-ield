from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from src.location.schema.dtos import locationAlertSchema
from src.trusted_contact.models.model import TrustedContactsModel
from src.user.models import UserModel

# Twillio setup
def send_sms(contact:TrustedContactsModel, message:str):
    pass


def alert(location:locationAlertSchema, db:Session, user:UserModel):
    Contacts = db.query(TrustedContactsModel).filter(
        user.id == TrustedContactsModel.userId
    ).all()

    if not Contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="contact not found")
    

    latitude = location.latitude
    longitude  = location.longitude

    location_link = (f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}")

    for contact in Contacts:
        message = f"""
                Emercengy Alert
                I need Help
                Live location : {location_link}"""
        send_sms(contact,message)

    return {"link" : location_link}

