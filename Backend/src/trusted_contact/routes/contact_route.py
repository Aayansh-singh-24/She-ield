from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.utils.db import get_db
from src.trusted_contact.schema.dtos import (
    TrustedContactCreateSchema,
    TrustedContactUpdate,
    TrustedContactResponse
)
from src.trusted_contact.controller import trusted_contact
from src.user.controller import is_authenticated
from src.user.models import UserModel


router = APIRouter(
    prefix="/trusted-contacts",
    tags=["Trusted Contacts"]
)


@router.post("/create_contact", response_model=TrustedContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact(
    data: TrustedContactCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(is_authenticated)
):
    return trusted_contact.add_contact(db, current_user, data)


@router.get("/read_contacts", response_model=list[TrustedContactResponse],status_code=status.HTTP_200_OK)
def read_contacts(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(is_authenticated)
):
    return trusted_contact.get_contacts(db, current_user)


@router.put("/edit_contact/{contact_id}", response_model=TrustedContactResponse, status_code=status.HTTP_200_OK)
def edit_contact(
    contact_id: int,
    data: TrustedContactUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(is_authenticated)
):
    return trusted_contact.update_contact(db, current_user, contact_id, data)


@router.delete("/remove_contact/{contact_id}",status_code=status.HTTP_204_NO_CONTENT)
def remove_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(is_authenticated)
):
    return trusted_contact.delete_contact(db, current_user, contact_id)