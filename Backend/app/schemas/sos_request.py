from pydantic import BaseModel


class LocationData(BaseModel):
    lat: float
    lng: float


class SOSTriggerRequest(BaseModel):
    userId: int
    threat_type: str
    confidence: float
    location: LocationData | None = None