from http import HTTPStatus

from src.user.dtos import UserSchema,LoginSchema
from sqlalchemy.orm import Session
from fastapi import HTTPException,Request,Depends
from src.user.models import UserModel
from src.utils.db import get_db
from pwdlib import PasswordHash
import jwt
from src.utils.settings import setting
from datetime import datetime,timedelta


password_hash=PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password,hashed_password):
    return password_hash.verify(plain_password,hashed_password)

def register(body:UserSchema,db:Session):
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
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def login_user(body:LoginSchema,db:Session):
    user=db.query(UserModel).filter(UserModel.username==body.username).first()
    if not user:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="You entered wrong username")
    
    if not verify_password(body.password,user.hash_password):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="You entered wrong password")
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