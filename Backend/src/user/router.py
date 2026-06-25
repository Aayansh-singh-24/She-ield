from http import HTTPStatus

from fastapi import APIRouter, Depends,Request
from sqlalchemy.orm import Session
from src.user.dtos import UserSchema,UserResponseSchema,LoginSchema
from src.utils.db import get_db
from src.user import controller

user_routes=APIRouter(prefix="/user", tags=["user"])

# @user_routes.get("/register")
# def get_register():
#     return {"message": "Use POST method to register a user", "schema": {"name": "string", "username": "string", "hash_password": "string", "email": "string"},"msg":"Registration done"}

@user_routes.post("/register", response_model=UserResponseSchema,status_code=HTTPStatus.CREATED) # type: ignore
def register(body:UserSchema, db:Session=Depends(get_db)):
    return controller.register(body, db)

@user_routes.post("/login",status_code=HTTPStatus.OK)
def login(body:LoginSchema,db:Session=Depends(get_db)):
    return controller.login_user(body,db)

@user_routes.get("/is_auth",status_code=HTTPStatus.OK,response_model=UserResponseSchema)
def is_auth(request:Request,db:Session=Depends(get_db)):
    return controller.is_authenticated(request,db)

