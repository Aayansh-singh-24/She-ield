from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from src.utils.db import Base

class AudioModel(Base):
    __tablename__ = "audio_table"
    id = Column(Integer,primary_key=True)
    filename = Column(String,nullable=False)
    filepath = Column(String,nullable=False)
    user_id = Column(Integer, ForeignKey("user_table.id", ondelete="CASCADE"))
    owner = relationship("UserModel", back_populates="audio")