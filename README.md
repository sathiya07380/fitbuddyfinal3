# ⚡ FitBuddy – AI Fitness Plan Generator using Gemini Models

FitBuddy is an intelligent, web-based health and fitness application that uses Google's **Gemini AI models** to generate hyper-personalized 7-day workout routines and targeted nutrition tips. Built with **FastAPI**, **SQLAlchemy ORM**, **SQLite**, and **Jinja2 Templates**, FitBuddy provides both an interactive web UI and RESTful API endpoints.

---

## 🎯 Core Scenarios Handled

1. **Scenario 1 (Personalized 7-Day Plan)**: A user submits personal details (Name, User ID, Age, Weight, Goal, Intensity) and receives a structured, day-by-day workout routine tailored to their objective.
2. **Scenario 2 (Feedback-Based Plan Refinement)**: Users can submit feedback on their active workout plan (e.g., *"add more yoga on weekends"*, *"reduce heavy squats"*, *"increase cardio"*). Gemini 1.5 Pro regenerates and updates their plan accordingly.
3. **Scenario 3 (Goal-Specific Nutrition Tips)**: Powered by Gemini Flash, users receive concise, actionable dietary guidance emphasizing protein requirements, hydration, and sleep hygiene.
4. **Scenario 4 (Coach / Admin Oversight)**: A dedicated admin panel (`/view-all-users`) allows trainers to view all registered users, examine their original plans, inspect updated plans with feedback history, and delete users when needed.

---

## 🏗️ Technical Architecture & Tech Stack

| Layer | Technology | Role |
|---|---|---|
| **Backend Framework** | **FastAPI** | High-performance routing, dependency injection, and Pydantic validation |
| **Server** | **Uvicorn** | Lightning-fast ASGI web server |
| **AI Models** | **Google Gemini 1.5 Pro** | 7-day workout plan generation & adaptive feedback updating |
| **AI Models** | **Google Gemini Flash** | Lightweight, high-speed nutrition and recovery tip generation |
| **Database** | **SQLite + SQLAlchemy ORM** | Relational data persistence for Users and Plans |
| **Frontend** | **HTML5 + CSS3 + Jinja2** | Responsive dark gym-themed user interface |

---

## 📂 Project Directory Structure

```text
fitbuddy/
│
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI application entrypoint & lifespan
│   ├── database.py              # SQLAlchemy models (User, Plan) & CRUD operations
│   ├── gemini_generator.py      # Workout plan generation (Gemini 1.5 Pro)
│   ├── gemini_flash_generator.py# Nutrition tip generation (Gemini Flash)
│   ├── updated_plan.py          # Feedback-based plan refinement (Gemini 1.5 Pro)
│   └── routes.py                # Core routes, form handlers & REST API endpoints
│
├── templates/
│   ├── index.html               # Main homepage form for user profile input
│   ├── result.html              # Plan display (<pre>), nutrition tip & feedback form
│   └── all_users.html           # Coach/Admin dashboard with original vs updated plans
│
├── static/
│   ├── css/
│   │   └── style.css            # Gym-themed dark UI styling with responsive design
│   └── images/                  # Static assets & images
│
├── .env                         # Environment variables (GOOGLE_API_KEY)
├── .env.example                 # Sample environment template
├── requirements.txt             # Python dependencies
├── main.py                      # Root proxy runner
├── test_app.py                  # Integration test suite
└── README.md                    # Documentation
```

---

## 🚀 Getting Started

### 1. Activate the Virtual Environment

On Windows:
```powershell
.\fitbuddy-env\Scripts\activate
```

### 2. Configure Google Gemini API Key

Open `.env` and paste your Gemini API key (obtainable free from [Google AI Studio](https://aistudio.google.com/)):
```env
GOOGLE_API_KEY=AIzaSyYourActualKeyHere
```
*(Note: If no API key is provided, FitBuddy includes a high-fidelity fallback generator so you can test all features offline without interruption).*

### 3. Run the Development Server

You can launch the server using any of the following commands:

```bash
uvicorn app.main:app --reload
```
or
```bash
uvicorn main:app --reload
```
or
```bash
python main.py
```

### 4. Access the Application

- **Web Application**: Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.
- **Coach / Admin View**: Open [http://127.0.0.1:8000/view-all-users](http://127.0.0.1:8000/view-all-users)
- **Interactive API Documentation (Swagger UI)**: Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Running Automated Tests

A complete verification test suite is included:

```powershell
.\fitbuddy-env\Scripts\python test_app.py
```
This tests:
- Database creation & CRUD operations (`save_user`, `save_plan`, `update_plan`, `get_original_plan`, `get_all_users`, `delete_user`)
- Gemini AI Generation logic & fallback routines
- All HTTP endpoints (`/`, `/generate-workout`, `/submit-feedback`, `/view-all-users`, `/api/generate-workout`)
