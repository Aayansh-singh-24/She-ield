from pydantic import BaseModel 

class UserSchema(BaseModel):
    name:str
    username:str
    password:str
    email:str


class UserResponseSchema(BaseModel):
    name:str
    username:str
    email:str
    id:int

class LoginSchema(BaseModel):
    username:str
    password:str
    
# In src/user/dtos.py
class VerifyOTPSchema(BaseModel):
    email: str
    otp_code: str

class ResendOTPSchema(BaseModel):
    email: str