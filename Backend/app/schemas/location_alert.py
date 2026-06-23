from pydantic import BaseModel

class locationAlertSchema(BaseModel):
    latitude : float
    longitude : float