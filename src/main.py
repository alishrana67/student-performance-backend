from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.schemas import Student
from src.predictor import predict_exam_score

app = FastAPI(title="Student Performance Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Student Performance Prediction API Running"}

@app.post("/predict")
def predict(student: Student):

    result = predict_exam_score(student.dict())

    return {
        "predicted_exam_score": result
    }