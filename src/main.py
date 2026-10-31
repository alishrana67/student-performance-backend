import logging
from typing import Optional

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from src.database import Base, engine, get_db
from src.models import PredictionRecord, User
from src.schemas import Student
from src.predictor import predict_exam_score
from src.auth import get_optional_current_user
from src.auth_routes import router as auth_router
from src.dashboard_routes import router as dashboard_router, determine_level

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("scoresense")

# Initialize database tables
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized successfully.")
except Exception as e:
    logger.error(f"Error initializing database: {e}")

app = FastAPI(
    title="Score Sense AI – Student Performance Prediction & Analytics API",
    description="Intelligent student performance prediction, secure authentication, and analytics dashboard.",
    version="2.0.0",
)

# CORS configuration supporting all local dev ports and all Vercel domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_origin_regex=r"^(https?://(localhost|127\.0\.0\.1)(:\d+)?|https://.*\.vercel\.app)$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Authentication and Dashboard routers
app.include_router(auth_router)
app.include_router(dashboard_router)


@app.get("/")
def home():
    return {
        "message": "Student Performance Prediction API Running",
        "version": "2.0.0",
        "docs_url": "/docs",
    }


@app.post("/predict")
def predict(
    student: Student,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db),
):
    """
    Predict student exam score using the ML pipeline.
    Maintains 100% backward compatibility with existing clients.
    Persists prediction to database for history and analytics tracking.
    """
    payload = student.dict()
    result = predict_exam_score(payload)
    perf_level = determine_level(result)

    record_id = None
    try:
        record = PredictionRecord(
            user_id=current_user.id if current_user else None,
            predicted_exam_score=result,
            performance_level=perf_level,
            **payload,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        record_id = record.id
    except Exception as e:
        logger.warning(f"Could not persist prediction to database: {e}")
        db.rollback()

    return {
        "predicted_exam_score": result,
        "performance_level": perf_level,
        "record_id": record_id,
    }
