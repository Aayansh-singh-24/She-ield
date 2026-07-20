from http import HTTPStatus

from src.user.dtos import UserSchema,LoginSchema
from sqlalchemy.orm import Session
from fastapi import HTTPException,Request,Depends,BackgroundTasks
from fastapi import WebSocket
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
    
    # Also check if username is currently pending in OTPVerificationModel and not expired
    pending_user=db.query(OTPVerificationModel).filter(
        OTPVerificationModel.username==body.username,
        OTPVerificationModel.expires_at > datetime.now()
    ).first()
    if pending_user:
        raise HTTPException(400,detail="Username is already registered and verification is pending...")

    is_user=db.query(UserModel).filter(UserModel.email==body.email).first()
    if is_user:
        raise HTTPException(400,detail="Email already exists...")
    
    hash_password=get_password_hash(body.password)

    # Generate and save OTP with user credentials in OTPVerificationModel instead of UserModel
    otp = generate_otp()
    expires_at = datetime.now() + timedelta(minutes=10)
    
    # Remove older OTPs / pending registrations for this email
    db.query(OTPVerificationModel).filter(OTPVerificationModel.email == body.email).delete()
    
    otp_entry = OTPVerificationModel(
        email=body.email,
        otp_code=otp,
        expires_at=expires_at,
        name=body.name,
        username=body.username,
        hash_password=hash_password
    )
    db.add(otp_entry)
    db.commit()

    # Send OTP in background
    background_tasks.add_task(send_otp_email, body.email, otp)

    # Return temporary user object to satisfy the UserResponseSchema response model
    return {
        "id": 0,
        "name": body.name,
        "username": body.username,
        "email": body.email
    }


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

    exp_time=datetime.now()+timedelta(minutes=setting.EXP_TIME)
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
    


async def websocket_authenticate(websocket:WebSocket, db:Session):
    token = websocket.headers.get("authorization")
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

    # Check if user already exists (fallback for existing user verification)
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if user:
        user.is_verified = True
        db.commit()
    elif otp_record.username:
        # Create user in UserModel since OTP is verified
        new_user = UserModel(
            name=otp_record.name or "",
            username=otp_record.username,
            hash_password=otp_record.hash_password or "",
            email=otp_record.email,
            is_verified=True
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    else:
        raise HTTPException(status_code=400, detail="Registration details missing in verification record")
        
    # Clean up OTP records
    db.query(OTPVerificationModel).filter(OTPVerificationModel.email == email).delete()
    db.commit()

    return {"message": "Email verified successfully"}

def resend_otp_code(email: str, db: Session, background_tasks: BackgroundTasks):
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if user and user.is_verified:
        return {"message": "Email is already verified"}

    # Find the pending registration in OTPVerificationModel
    pending_reg = db.query(OTPVerificationModel).filter(OTPVerificationModel.email == email).first()
    if not user and not pending_reg:
        raise HTTPException(status_code=404, detail="User registration not found")

    # Generate and update OTP
    otp = generate_otp()
    expires_at = datetime.now() + timedelta(minutes=10)
    
    if pending_reg:
        pending_reg.otp_code = otp
        pending_reg.expires_at = expires_at
    else:
        # User exists but is unverified (fallback for existing users)
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