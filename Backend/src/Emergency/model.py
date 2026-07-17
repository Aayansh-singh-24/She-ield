from uuid import uuid4
from sqlalchemy import Column, String, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.utils.db import Base

class EmergencySession(Base):
    __tablename__ = "emergency_session"

    id = Column(Integer, primary_key=True)
    session_id = Column(String, unique=True, nullable=False, default=str(uuid4()))
    status = Column(String, default="Active")
    started_time = Column(DateTime(timezone=True), server_default=func.now())
    ended_time = Column(DateTime(timezone=True), nullable=True)
    user_id = Column(Integer, ForeignKey("user_table.id",ondelete="CASCADE"))

    owner = relationship("UserModel", back_populates="emergency_session") # showing connection with user table

    location = relationship("LocationHistory", back_populates="session", passive_deletes=True, cascade="all, delete", order_by="LocationHistory.timestamp") # showing connection with LocationHistory table


class LocationHistory(Base):
    __tablename__ = "location_history"
    id = Column(Integer, primary_key=True)
    session_id = Column(String, ForeignKey("emergency_session.session_id", ondelete="CASCADE"))
    latitude = Column(String, nullable=False)
    longitude = Column(String, nullable=False)
    speed = Column(Float,nullable=False)
    accuracy = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True),nullable=False, server_default=func.now())

    session = relationship("EmergencySession",back_populates="location")
