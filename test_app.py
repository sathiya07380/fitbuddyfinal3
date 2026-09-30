import os
import sys
from fastapi.testclient import TestClient

# Ensure root directory is on Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app
from app.database import (
    init_db,
    save_user,
    save_plan,
    update_plan,
    get_user,
    get_plan,
    get_original_plan,
    get_all_users,
    delete_user,
)
from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan


def run_tests():
    print("=== 1. Testing Database & ORM Functions ===")
    init_db()

    # Test user save & get
    user = save_user(
        username="Test Athlete",
        user_id="TEST-001",
        age=28,
        weight=75.0,
        goal="Muscle Gain & Hypertrophy",
        intensity="high",
    )
    assert user is not None, "Failed to save user"
    assert user.username == "Test Athlete"
    print("[PASS] save_user succeeded")

    fetched_user = get_user("TEST-001")
    assert fetched_user is not None and fetched_user.user_id == "TEST-001"
    print("[PASS] get_user succeeded")

    # Test plan save & get
    plan = save_plan(
        user_id="TEST-001",
        original_plan="Day 1: Chest & Triceps\nDay 2: Back & Biceps\nDay 3: Rest",
        nutrition_tip="Eat 150g protein daily",
    )
    assert plan is not None
    orig = get_original_plan("TEST-001")
    assert "Day 1:" in orig
    print("[PASS] save_plan & get_original_plan succeeded")

    # Test plan update
    updated = update_plan(
        user_id="TEST-001",
        updated_plan="Day 1: Chest & Triceps\nDay 2: Back & Biceps\nDay 3: Yoga & Recovery",
        feedback="Include yoga on Day 3",
    )
    assert updated.updated_plan is not None
    assert "Yoga" in updated.updated_plan
    print("[PASS] update_plan succeeded")

    users_list = get_all_users()
    assert len(users_list) >= 1
    print(f"[PASS] get_all_users returned {len(users_list)} records")

    print("\n=== 2. Testing AI Generator Functions ===")
    plan_text = generate_workout_gemini(
        goal="Weight Loss",
        intensity="medium",
        age=30,
        weight=80.0,
        username="Sarah",
    )
    assert "DAY 1:" in plan_text
    assert "DAY 7:" in plan_text
    print("[PASS] generate_workout_gemini generated 7-day plan")

    tip_text = generate_nutrition_tip_with_flash(
        goal="Weight Loss",
        age=30,
        weight=80.0,
    )
    assert len(tip_text) > 20
    print("[PASS] generate_nutrition_tip_with_flash generated nutrition tips")

    revised_text = update_workout_plan(
        original_plan=plan_text,
        feedback="Include more yoga and stretching on weekends",
        goal="Weight Loss",
        intensity="medium",
    )
    assert len(revised_text) > 50
    print("[PASS] update_workout_plan generated revised plan")

    print("\n=== 3. Testing FastAPI HTTP Endpoints via TestClient ===")
    client = TestClient(app)

    # Test GET /
    res_home = client.get("/")
    assert res_home.status_code == 200
    assert "FitBuddy" in res_home.text
    assert "Generate My 7-Day Plan" in res_home.text
    print("[PASS] GET / returned 200 and rendered index.html")

    # Test POST /generate-workout
    res_gen = client.post(
        "/generate-workout",
        data={
            "username": "David Miller",
            "user_id": "FIT-7788",
            "age": 29,
            "weight": 82.5,
            "goal": "Muscle Gain & Hypertrophy",
            "intensity": "high",
        },
    )
    assert res_gen.status_code == 200
    assert "David Miller" in res_gen.text
    assert "FIT-7788" in res_gen.text
    assert "7-Day Workout" in res_gen.text
    print("[PASS] POST /generate-workout returned 200 and rendered result.html")

    # Test POST /submit-feedback
    res_fb = client.post(
        "/submit-feedback",
        data={
            "user_id": "FIT-7788",
            "feedback": "Add 30 minutes of yoga on Day 3 and reduce heavy squats",
        },
    )
    assert res_fb.status_code == 200
    assert "Workout plan successfully updated" in res_fb.text
    assert "FIT-7788" in res_fb.text
    print("[PASS] POST /submit-feedback returned 200 and updated plan")

    # Test GET /view-all-users
    res_admin = client.get("/view-all-users")
    assert res_admin.status_code == 200
    assert "FIT-7788" in res_admin.text
    assert "David Miller" in res_admin.text
    print("[PASS] GET /view-all-users returned 200 and displayed admin table")

    # Test JSON APIs
    res_api = client.post(
        "/api/generate-workout",
        json={
            "username": "API Tester",
            "user_id": "API-101",
            "age": 24,
            "weight": 68.0,
            "goal": "General Wellness",
            "intensity": "low",
        },
    )
    assert res_api.status_code == 200
    json_data = res_api.json()
    assert json_data["status"] == "success"
    assert "workout_plan" in json_data
    print("[PASS] POST /api/generate-workout returned 200 with JSON payload")

    # Test Feature walkthrough pages
    for f_key in ["gemini-pro", "gemini-flash", "feedback-loop", "admin-oversight"]:
        res_f = client.get(f"/features/{f_key}")
        assert res_f.status_code == 200, f"Failed for feature {f_key}"
        assert "FitBuddy" in res_f.text
    print("[PASS] GET /features/* returned 200 for all 4 feature pages")

    # Test GET /user-plan/{user_id}
    res_up = client.get("/user-plan/FIT-7788")
    assert res_up.status_code == 200
    assert "David Miller" in res_up.text
    print("[PASS] GET /user-plan/FIT-7788 returned 200 and rendered athlete plan")

    # Test Delete User
    del_ok = delete_user("TEST-001")
    assert del_ok is True
    print("[PASS] delete_user succeeded")

    print("\nALL TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    run_tests()
