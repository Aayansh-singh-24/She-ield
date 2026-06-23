from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.utils.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phoneNo = Column(String, unique=True, index=True, nullable=False)

    trusted_contacts = relationship(
        "TrustedContactsModel",
        back_populates="owner",
        cascade="all, delete"
    )