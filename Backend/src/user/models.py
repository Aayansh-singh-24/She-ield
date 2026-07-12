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
    is_verified = Column(Boolean, default=False, nullable=False)

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

    profile = relationship(
        "ProfileModel",
        back_populates="owner",
        cascade="all,delete"
    )

class OTPVerificationModel(Base):
    __tablename__ = "otp_verification"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False)
    otp_code = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    hash_password = Column(String, nullable=True)
