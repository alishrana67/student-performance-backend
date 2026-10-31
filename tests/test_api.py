import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from src.main import home, predict
from src.database import SessionLocal, Base, engine
from src.models import User, PredictionRecord
from src.schemas import Student, UserRegister, UserLogin
from src.auth_routes import signup, login, get_me
from src.dashboard_routes import (
    get_dashboard_overview,
    get_dashboard_analytics,
    get_prediction_history,
    get_insights,
    determine_level,
)


def run_all_tests():
    print("--- Starting Backend API Test Suite ---")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Health check
        res = home()
        assert "Student Performance Prediction API Running" in res["message"]
        print("[PASS] 1. Health check endpoint")

        # 2. Authentication: Signup
        test_email = "alex_test_suite@example.com"
        db.query(User).filter(User.email == test_email).delete()
        db.commit()

        signup_data = UserRegister(name="Alex Carter", email=test_email, password="StrongPassword123!")
        reg_result = signup(signup_data, db=db)
        assert "access_token" in reg_result
        assert reg_result["user"].email == test_email
        print("[PASS] 2. User registration & JWT generation")

        # 3. Authentication: Login
        login_data = UserLogin(email=test_email, password="StrongPassword123!")
        login_result = login(login_data, db=db)
        token = login_result["access_token"]
        assert token is not None
        print("[PASS] 3. User login & token generation")

        # 4. Authentication: Profile /auth/me
        current_user = db.query(User).filter(User.email == test_email).first()
        me_result = get_me(current_user=current_user)
        assert me_result.name == "Alex Carter"
        print("[PASS] 4. Authenticated profile retrieval")

        # 5. Prediction: Anonymous
        sample_data = {
            "Hours_Studied": 6.0,
            "Attendance": 98.0,
            "Parental_Involvement": "Medium",
            "Access_to_Resources": "Medium",
            "Extracurricular_Activities": "No",
            "Sleep_Hours": 7.0,
            "Previous_Scores": 88.0,
            "Motivation_Level": "Low",
            "Internet_Access": "Yes",
            "Tutoring_Sessions": 5,
            "Family_Income": "Medium",
            "Teacher_Quality": "Low",
            "School_Type": "Public",
            "Peer_Influence": "Positive",
            "Physical_Activity": 3.0,
            "Learning_Disabilities": "No",
            "Parental_Education_Level": "College",
            "Distance_from_Home": "Near",
            "Gender": "Male",
        }
        student_schema = Student(**sample_data)
        pred_res = predict(student=student_schema, current_user=None, db=db)
        assert "predicted_exam_score" in pred_res
        assert 0 <= pred_res["predicted_exam_score"] <= 120
        assert pred_res["performance_level"] in ["Excellent", "Very Good", "Good", "Needs Improvement"]
        print("[PASS] 5. Anonymous prediction & ML inference")

        # 6. Prediction: Authenticated (persists to user history)
        pred_auth_res = predict(student=student_schema, current_user=current_user, db=db)
        assert pred_auth_res["record_id"] is not None
        saved_rec = db.query(PredictionRecord).filter(PredictionRecord.id == pred_auth_res["record_id"]).first()
        assert saved_rec.user_id == current_user.id
        print("[PASS] 6. Authenticated prediction persistence with user linkage")

        # 7. Dashboard Overview
        overview = get_dashboard_overview(db=db)
        assert overview["total_records"] >= 6607
        assert overview["avg_predicted_score"] > 0
        print("[PASS] 7. Dashboard overview metrics")

        # 8. Dashboard Analytics
        analytics = get_dashboard_analytics(db=db)
        assert len(analytics.score_distribution) == 5
        assert len(analytics.performance_level_distribution) == 4
        print("[PASS] 8. Dashboard analytics & Recharts aggregations")

        # 9. Prediction History
        history = get_prediction_history(page=1, page_size=5, user_only=True, current_user=current_user, db=db)
        assert history.total >= 1
        assert len(history.items) >= 1
        print("[PASS] 9. Prediction history pagination & filtering")

        # 10. Empirical Insights
        insights = get_insights()
        assert len(insights) >= 4
        print("[PASS] 10. Data-backed empirical insights")

        print("--- ALL 10 TESTS PASSED SUCCESSFULLY! ---")

    finally:
        db.close()


if __name__ == "__main__":
    run_all_tests()
