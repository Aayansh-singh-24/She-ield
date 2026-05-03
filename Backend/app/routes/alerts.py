from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.sos_request import SOSTriggerRequest
from app.services.trusted_contact_service import get_sos_contacts


router = APIRouter(prefix="/alert", tags=["ML Alerts"])


@router.post("/sos_trigger")
def trigger_sos_from_ml(
    data: SOSTriggerRequest,
    db: Session = Depends(get_db)
):
    contacts = get_sos_contacts(db, data.userId)

    if not contacts:
        raise HTTPException(
            status_code=404,
            detail=f"No SOS contacts found for user_id {data.userId}"
        )

    sos_numbers = [
        {
            "name": con.name,
            "country_code": con.country_code,
            "phone_no": con.phoneNo,
            "full_number": f"{con.country_code}{con.phoneNo}"
        }
        for con in contacts
    ]

    return {
        "message": "SOS contacts fetched successfully",
        "user_id": data.userId,
        "threat_type": data.threat_type,
        "confidence": data.confidence,
        "location": data.location,
        "sos_contacts": sos_numbers
    }