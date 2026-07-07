from http import HTTPStatus

from src.user.dtos import UserSchema,LoginSchema
from sqlalchemy.orm import Session
from fastapi import HTTPException,Request,Depends,BackgroundTasks
from src.user.models import UserModel, OTPVerificationModel
from src.utils.db import get_db
from pwdlib import PasswordHash
import jwt
from src.utils.settings import setting
from datetime import datetime,timedelta
import random
from src.utils.helpers import send_otp_email

password_hash=PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password,hashed_password):
    return password_hash.verify(plain_password,hashed_password)

def register(body:UserSchema,db:Session,background_tasks:BackgroundTasks):
    is_user=db.query(UserModel).filter(UserModel.username==body.username).first()
    if is_user:
        raise HTTPException(400,detail="Username already exists...")
    
    is_user=db.query(UserModel).filter(UserModel.email==body.email).first()
    if is_user:
        raise HTTPException(400,detail="Email already exists...")
    
    hash_password=get_password_hash(body.password)

    new_user=UserModel(
        name=body.name,
        username=body.username,
        hash_password=hash_password,
        email=body.email,
        is_verified=False  # default unverified
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

     # Generate and save OTP
    otp = generate_otp()
    expires_at = datetime.now() + timedelta(minutes=10)
    
    otp_entry = OTPVerificationModel(
        email=body.email,
        otp_code=otp,
        expires_at=expires_at
    )
    db.add(otp_entry)
    db.commit()

    # Send OTP in background
    background_tasks.add_task(send_otp_email, body.email, otp)

    return new_user

def login_user(body:LoginSchema,db:Session):
    user=db.query(UserModel).filter(UserModel.username==body.username).first()
    if not user:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="You entered wrong username")
    
    if not verify_password(body.password,user.hash_password):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="You entered wrong password")
      # Check if verified
    if not user.is_verified:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, 
            detail="Your email is not verified. Please verify using OTP."
        )

    exp_time=datetime.now()+timedelta(minutes=30)
    token=jwt.encode({"_id":user.id,"exp":exp_time.timestamp()},setting.SECRET_KEY,setting.ALGORITHM)


    return {
        "token":token
    }



## Token send - 

def is_authenticated(request:Request,db:Session=Depends(get_db)):
    token=request.headers.get("authorization")
    if not token:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Authorization header missing")
    token=token.split(" ")[-1]
    try:
        data=jwt.decode(token,setting.SECRET_KEY,setting.ALGORITHM)
        # print(data)
        user_id=data.get("_id")
        exp_time=int(data["exp"])
        current_time=datetime.now().timestamp()
        if current_time>exp_time:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,detail="You are unauthorized.")


        user=db.query(UserModel).filter(UserModel.id==user_id).first()
        if not user:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,detail="You are unauthorized.")

        
        return user
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token")
    


    ## otp ke liye

def generate_otp() -> str:
    return f"{random.randint(100000, 999999)}"


def verify_otp_code(email: str, otp_code: str, db: Session):
    # Find active non-expired OTP record
    otp_record = db.query(OTPVerificationModel).filter(
        OTPVerificationModel.email == email,
        OTPVerificationModel.otp_code == otp_code
    ).order_by(OTPVerificationModel.id.desc()).first()

    if not otp_record:
        raise HTTPException(status_code=400, detail="Invalid OTP code")

    if datetime.now() > otp_record.expires_at:
        db.delete(otp_record)
        db.commit()
        raise HTTPException(status_code=400, detail="OTP code has expired")

    # Mark user as verified
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if user:
        user.is_verified = True
        db.commit()
        
    # Clean up OTP records
    db.query(OTPVerificationModel).filter(OTPVerificationModel.email == email).delete()
    db.commit()

    return {"message": "Email verified successfully"}

def resend_otp_code(email: str, db: Session, background_tasks: BackgroundTasks):
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if user.is_verified:
        return {"message": "Email is already verified"}

    # Generate and update OTP
    otp = generate_otp()
    expires_at = datetime.now() + timedelta(minutes=10)
    
    # Remove older OTPs for this email
    db.query(OTPVerificationModel).filter(OTPVerificationModel.email == email).delete()
    
    otp_entry = OTPVerificationModel(
        email=email,
        otp_code=otp,
        expires_at=expires_at
    )
    db.add(otp_entry)
    db.commit()

    background_tasks.add_task(send_otp_email, email, otp)
    return {"message": "OTP resent successfully"}