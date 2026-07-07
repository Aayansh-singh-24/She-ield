from src.utils.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped,  mapped_column
from src.user.models import UserModel

# This is way to write model in sqlalchemy version 2.x 

class ProfileModel(Base):
    __tablename__ = "profile_table"
    id : Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    filename : Mapped[str] = mapped_column(String,nullable=False)
    storage_key : Mapped[str] = mapped_column(String,nullable=False)
    content_type : Mapped[str] = mapped_column(String,nullable=False)
    user_id : Mapped[str] = mapped_column(Integer,ForeignKey("user_table.id",ondelete="CASCADE"))

    owner : Mapped[UserModel] = relationship("UserModel",back_populates="profile")
    