from fastapi import HTTPException,status,BackgroundTasks
from sqlalchemy.orm import Session
from src.location.schema.dtos import locationAlertSchema
from src.trusted_contact.models.model import TrustedContactsModel
from src.user.models import UserModel
import twilio
# Twillio setup
from dotenv import load_dotenv
import os

load_dotenv()

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
PHONE = os.getenv("TWILIO_PHONE_NUMBER")
from twilio.rest import Client


client = Client(ACCOUNT_SID, AUTH_TOKEN)


# print(message.sid)
# def send_sms(phoneNo:TrustedContactsModel, message:str):
def send_sms(phone_no:str,message_body:str):
    try:
     message = client.messages.create(
     body=message_body,
     from_=PHONE,
     to=phone_no
     )
     print(f"SMS successfully sent to {phone_no}")
    except Exception as e:
        print(f"Failed to send SMS to {phone_no}: {str(e)}")


def alert(location:locationAlertSchema, background_task:BackgroundTasks, db:Session, current_user:UserModel):

    Contacts = db.query(TrustedContactsModel).filter(
        current_user.id == TrustedContactsModel.userId
    ).all()

    if not Contacts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="contact not found")
    

    latitude = location.latitude
    longitude  = location.longitude
    custom_msg = location.message or "I need Help!!"

    location_link = (f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}")

    for contact in Contacts:
        message_body = f"""
                Emercengy Alert!
                \n{custom_msg}\n
                Live location : {location_link}"""
        country_code = contact.country_code or "+91"
        if not country_code_str.startswith("+"):
            country_code_str = "+" + country_code_str
        phone_no = f"{country_code}{contact.phoneNo}"
        
        background_task.add_task(send_sms,phone_no, message_body)

        # send_sms(phone_no, message_body)

        # send_sms(contact,message)

    return {"link" : location_link}