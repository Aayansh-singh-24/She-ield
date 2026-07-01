from sqlalchemy import Column, String ,Integer,DateTime, Boolean
from sqlalchemy.orm import relationship

from src.utils.db import Base

class UserModel(Base):
    __tablename__="user_table"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    username=Column(String,nullable=False, index=True)
    hash_password=Column(String,nullable=False)
    email=Column(String)

    trusted_contacts = relationship(
        "TrustedContactsModel",
        back_populates="owner",
        cascade="all, delete"
    )
    


    audio = relationship(
        "AudioModel",
        back_populates="owner",
        cascade="all,delete"
    )


    