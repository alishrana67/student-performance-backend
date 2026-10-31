from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="student", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    predictions = relationship("PredictionRecord", back_populates="user", cascade="all, delete-orphan")


class PredictionRecord(Base):
    __tablename__ = "prediction_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True, nullable=False)

    # 19 Input Features
    Hours_Studied = Column(Float, nullable=False)
    Attendance = Column(Float, nullable=False)
    Parental_Involvement = Column(String(50), nullable=False)
    Access_to_Resources = Column(String(50), nullable=False)
    Extracurricular_Activities = Column(String(50), nullable=False)
    Sleep_Hours = Column(Float, nullable=False)
    Previous_Scores = Column(Float, nullable=False)
    Motivation_Level = Column(String(50), nullable=False)
    Internet_Access = Column(String(50), nullable=False)
    Tutoring_Sessions = Column(Integer, nullable=False)
    Family_Income = Column(String(50), nullable=False)
    Teacher_Quality = Column(String(50), nullable=False)
    School_Type = Column(String(50), nullable=False)
    Peer_Influence = Column(String(50), nullable=False)
    Physical_Activity = Column(Float, nullable=False)
    Learning_Disabilities = Column(String(50), nullable=False)
    Parental_Education_Level = Column(String(50), nullable=False)
    Distance_from_Home = Column(String(50), nullable=False)
    Gender = Column(String(50), nullable=False)

    # Output predictions
    predicted_exam_score = Column(Float, nullable=False)
    performance_level = Column(String(50), nullable=False)

    user = relationship("User", back_populates="predictions")
