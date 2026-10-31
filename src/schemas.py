from datetime import datetime
import re
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


# ---------------- Existing Student Schema (DO NOT CHANGE) ----------------
class Student(BaseModel):
    Hours_Studied: float
    Attendance: float
    Parental_Involvement: str
    Access_to_Resources: str
    Extracurricular_Activities: str
    Sleep_Hours: float
    Previous_Scores: float
    Motivation_Level: str
    Internet_Access: str
    Tutoring_Sessions: int
    Family_Income: str
    Teacher_Quality: str
    School_Type: str
    Peer_Influence: str
    Physical_Activity: float
    Learning_Disabilities: str
    Parental_Education_Level: str
    Distance_from_Home: str
    Gender: str


EMAIL_REGEX = re.compile(r"^[\w\.\+\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z0-9\-\.]+$")


# ---------------- Auth Schemas ----------------
class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., min_length=5, max_length=255)
    password: str = Field(..., min_length=6, max_length=100)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        clean_email = v.strip().lower()
        if not EMAIL_REGEX.match(clean_email):
            raise ValueError("Invalid email format")
        return clean_email


class UserLogin(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        clean_email = v.strip().lower()
        if not EMAIL_REGEX.match(clean_email):
            raise ValueError("Invalid email format")
        return clean_email


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ---------------- Prediction API Schemas ----------------
class PredictionResponse(BaseModel):
    predicted_exam_score: float
    performance_level: Optional[str] = None
    record_id: Optional[int] = None


class PredictionHistoryItem(BaseModel):
    id: int
    created_at: datetime
    predicted_exam_score: float
    performance_level: str
    Hours_Studied: float
    Attendance: float
    Previous_Scores: float
    Parental_Involvement: str
    Access_to_Resources: str
    Motivation_Level: str
    Teacher_Quality: str
    Family_Income: str
    School_Type: str
    Gender: str
    Sleep_Hours: float
    Tutoring_Sessions: int
    Physical_Activity: float
    Internet_Access: str
    Extracurricular_Activities: str
    Peer_Influence: str
    Learning_Disabilities: str
    Parental_Education_Level: str
    Distance_from_Home: str

    class Config:
        from_attributes = True


class PaginatedPredictionHistory(BaseModel):
    items: List[PredictionHistoryItem]
    total: int
    page: int
    page_size: int
    total_pages: int


# ---------------- Dashboard Analytics Schemas ----------------
class DashboardOverview(BaseModel):
    total_records: int
    total_predictions: int
    avg_predicted_score: float
    max_predicted_score: float
    min_predicted_score: float
    avg_study_hours: float
    avg_attendance: float


class DistributionItem(BaseModel):
    range: str
    count: int
    percentage: float


class ScatterPoint(BaseModel):
    x: float
    y: float
    level: Optional[str] = None


class LevelDistributionItem(BaseModel):
    level: str
    count: int
    color: str


class FactorImpactItem(BaseModel):
    factor: str
    label: str
    high_label: str
    high_score: float
    low_label: str
    low_score: float
    difference: float


class DashboardAnalytics(BaseModel):
    score_distribution: List[DistributionItem]
    study_hours_vs_score: List[ScatterPoint]
    attendance_vs_score: List[ScatterPoint]
    performance_level_distribution: List[LevelDistributionItem]
    previous_vs_predicted: List[ScatterPoint]
    factor_impacts: Optional[List[FactorImpactItem]] = None


class InsightItem(BaseModel):
    id: str
    title: str
    summary: str
    stat: str
    category: str
    impact: str
