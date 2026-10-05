from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.utils.db import Base


class TrustedContactsModel(Base):
    __tablename__ = "trusted_contact"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey("user_table.id"), nullable=False,index=True)
    name = Column(String, nullable=False)
    email=Column(String,index=True,nullable=False)
    isSOS = Column(Boolean, default=False)

    owner = relationship("UserModel", back_populates="trusted_contacts")


