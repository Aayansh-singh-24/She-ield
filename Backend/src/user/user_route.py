from http import HTTPStatus

from fastapi import APIRouter, Depends,Request,BackgroundTasks
from sqlalchemy.orm import Session
from src.user.dtos import UserSchema,UserResponseSchema,LoginSchema,VerifyOTPSchema, ResendOTPSchema
from src.utils.db import get_db
from src.user import controller

router=APIRouter(prefix="/user", tags=["user"])

# @user_routes.get("/register")
# def get_register():
#     return {"message": "Use POST method to register a user", "schema": {"name": "string", "username": "string", "hash_password": "string", "email": "string"},"msg":"Registration done"}

@router.post("/register", response_model=UserResponseSchema,status_code=HTTPStatus.CREATED) # type: ignore
def register(body:UserSchema,background_tasks:BackgroundTasks, db:Session=Depends(get_db)):
    return controller.register(body, db, background_tasks)

@router.post("/verify-otp",status_code=HTTPStatus.OK)
def verif_otp(body:VerifyOTPSchema,db:Session=Depends(get_db)):
    return controller.verify_otp_code(body.email,body.otp_code,db)

@router.post("/resend-otp", status_code=HTTPStatus.OK)
def resend_otp(body: ResendOTPSchema, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    return controller.resend_otp_code(body.email, db, background_tasks)


@router.post("/login",status_code=HTTPStatus.OK)
def login(body:LoginSchema,db:Session=Depends(get_db)):
    return controller.login_user(body,db)

@router.get("/is_auth",status_code=HTTPStatus.OK,response_model=UserResponseSchema)
def is_auth(request:Request,db:Session=Depends(get_db)):
    return controller.is_authenticated(request,db)

