from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EmergencySessionCreate(BaseModel):
    message: Optional[str] = None


class EmergencySessionResponse(BaseModel):
    session_id: str
    status: str
    started_at: datetime

    class Config:
        from_attributes = True


class LiveLocationSchema(BaseModel):
    latitude: float
    longitude: float
    speed: Optional[float] = None
    accuracy: Optional[float] = None


class LocationHistoryResponse(BaseModel):
    latitude: float
    longitude: float
    speed: Optional[float]
    accuracy: Optional[float]
    timestamp: datetime

    class Config:
        from_attributes = True