from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.utils.database import Base


class TrustedContactsModel(Base):
    __tablename__ = "trusted_contact"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey("user.id"), nullable=False)
    name = Column(String, nullable=False)
    country_code = Column(String, default="+91")
    phoneNo = Column(String, nullable=False)
    isSOS = Column(Boolean, default=False)

    owner = relationship("User", back_populates="trusted_contacts")