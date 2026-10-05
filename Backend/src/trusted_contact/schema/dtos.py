from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, EmailStr


class TrustedContactCreateSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr =Field(...)
    is_sos_contact: bool = False


class TrustedContactUpdate(BaseModel):
    name: str
    email:EmailStr
    is_sos_contact: Optional[bool] = None
    

class TrustedContactResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    isSOS: bool