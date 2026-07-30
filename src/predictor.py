import joblib
import pandas as pd
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "student_performance_pipeline.pkl"


def load_model():
    return joblib.load(MODEL_PATH)


def predict_exam_score(payload: dict) -> float:
    model = load_model()
    input_df = pd.DataFrame([payload])
    prediction = model.predict(input_df)
    return float(prediction[0])
