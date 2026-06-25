from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.trusted_contact.models.model import TrustedContactsModel
from src.trusted_contact.schema.dtos import TrustedContactCreateSchema, TrustedContactUpdate



def validate_phone_number(phone_number: str):
    if not phone_number.isdigit():
        raise HTTPException(
            status_code=400,
            detail="Phone number must contain only digits"
        )

    if len(phone_number) != 10:
        raise HTTPException(
            status_code=400,
            detail="Phone number must be 10 digits"
        )


def add_contact(db: Session, user_id: int, data: TrustedContactCreateSchema):
    validate_phone_number(data.phone_number)

    existing_contact = db.query(TrustedContactsModel).filter(
        TrustedContactsModel.userId == user_id,
        TrustedContactsModel.phoneNo == data.phone_number
    ).first()
    
    if existing_contact:
        raise HTTPException(
            status_code=400,
            detail="Contact already exists"
        )

    contact = TrustedContactsModel(
        userId=user_id,
        name=data.name,
        phoneNo=data.phone_number,
        isSOS=data.is_sos_contact
    )

    db.add(contact)
    db.commit()
    db.refresh(contact)

    return contact


def get_contacts(db: Session, user_id: int):
    return db.query(TrustedContactsModel).filter(
        TrustedContactsModel.userId == user_id
    ).all()


# def get_sos_contacts(db: Session, user_id: int):
#     return db.query(TrustedContacts).filter(
#         TrustedContacts.userId == user_id,
#         TrustedContacts.isSOS.is_(True)
#     ).all()


def update_contact(db: Session, user_id: int, contact_id: int, data: TrustedContactUpdate):
    contact = db.query(TrustedContactsModel).filter(
        TrustedContactsModel.id == contact_id,
        TrustedContactsModel.userId == user_id
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

    if data.phone_number is not None:
        validate_phone_number(data.phone_number)

        existing_contact = db.query(TrustedContactsModel).filter(
            TrustedContactsModel.userId == user_id,
            TrustedContactsModel.phoneNo == data.phone_number,
            TrustedContactsModel.id != contact_id
        ).first()

        if existing_contact:
            raise HTTPException(
                status_code=400,
                detail="Contact number already exists"
            )

        contact.phoneNo = data.phone_number # type: ignore

    if data.is_sos_contact is not None:
        contact.isSOS = data.is_sos_contact # type: ignore

    db.commit()
    db.refresh(contact)

    return contact


def delete_contact(db: Session, user_id: int, contact_id: int):
    contact = db.query(TrustedContactsModel).filter(
        TrustedContactsModel.id == contact_id,
        TrustedContactsModel.userId == user_id
    ).first()

    if not contact:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )

    db.delete(contact)
    db.commit()

    return None