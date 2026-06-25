from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class TrustedContactCreateSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    phone_number: str = Field(..., min_length=10, max_length=10)
    is_sos_contact: bool = False


class TrustedContactUpdate(BaseModel):
    name: Optional[str] = None
    country_code: Optional[str] = None
    phone_number: Optional[str] = None
    is_sos_contact: Optional[bool] = None


class TrustedContactResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    country_code: str
    phoneNo: str
    isSOS: bool