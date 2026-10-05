from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.trusted_contact.models.model import TrustedContactsModel
from src.trusted_contact.schema.dtos import TrustedContactCreateSchema, TrustedContactUpdate
from src.user.models import UserModel


from fastapi import HTTPException


def add_contact(db: Session, current_user: UserModel, data: TrustedContactCreateSchema):

    existing_contact = db.query(TrustedContactsModel).filter(
        TrustedContactsModel.userId == current_user.id,
        TrustedContactsModel.emaiL == data.email
    ).first()
    
    if existing_contact:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    contact = TrustedContactsModel(
        userId=current_user.id,
        name=data.name,
        email=data.email,
        isSOS=data.is_sos_contact
    )

    db.add(contact)
    db.commit()
    db.refresh(contact)

    return contact


def get_contact(db: Session, current_user: UserModel):
    return db.query(TrustedContactsModel).filter(
        TrustedContactsModel.userId == current_user.id
    ).all()


# def get_sos_contacts(db: Session, user_id: int):
#     return db.query(TrustedContacts).filter(
#         TrustedContacts.userId == user_id,
#         TrustedContacts.isSOS.is_(True)
#     ).all()


def update_contact(db: Session, current_user: UserModel, email_id: int, data: TrustedContactUpdate):
    contact = db.query(TrustedContactsModel).filter(
        TrustedContactsModel.id == email_id,
        TrustedContactsModel.userId == current_user.id
    ).first()

    if not contact:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )

    if data.name is not None:
        contact.name = data.name # type: ignore

    if data.country_code is not None:
        contact.country_code = data.country_code # type: ignore

    if data.email is not None:

        existing_contact = db.query(TrustedContactsModel).filter(
            TrustedContactsModel.userId == current_user.id,
            TrustedContactsModel.email == data.email,
            TrustedContactsModel.id != email_id
        ).first()

        if existing_contact:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

        contact.email = data.email # type: ignore

    if data.is_sos_contact is not None:
        contact.isSOS = data.is_sos_contact # type: ignore

    db.commit()
    db.refresh(contact)

    return contact


def delete_contact(db: Session, current_user: UserModel, email_id: int):
    contact = db.query(TrustedContactsModel).filter(
        TrustedContactsModel.id == email_id,
        TrustedContactsModel.userId == current_user.id
    ).first()

    if not contact:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )

    db.delete(contact)
    db.commit()

    return None