from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

# MongoDB connection
app.config["MONGO_URI"] = "mongodb+srv://adityapatidar1810_db_user:Df8mECWr19ZmIs8O@cluster0.c3ofyk3.mongodb.net/academic_db?retryWrites=true&w=majority"
mongo = PyMongo(app)


# -------------------------
# HOME ROUTE
# -------------------------
@app.route("/")
def home():
    return "AI Study Planner Backend Running"


# -------------------------
# PREDICTION API
# -------------------------
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    study_hours = data.get("study_hours")
    attendance = data.get("attendance")
    sleep_hours = data.get("sleep_hours")

    # -------------------------
    # Prediction Logic
    # -------------------------
    predicted_score = (
        (study_hours * 5) +
        (attendance * 0.4) +
        (sleep_hours * 2)
    )

    # -------------------------
    # Risk Level
    # -------------------------
    if predicted_score < 50:
        risk = "High"
    elif predicted_score < 75:
        risk = "Medium"
    else:
        risk = "Low"

    # -------------------------
    # Burnout Detection
    # -------------------------
    if sleep_hours < 5 and study_hours > 7:
        burnout = "High"
    elif sleep_hours < 6:
        burnout = "Medium"
    else:
        burnout = "Low"

    # -------------------------
    # Productivity Score
    # -------------------------
    productivity_score = (
        (study_hours * 10) +
        (attendance * 0.3) +
        (sleep_hours * 5)
    ) / 2

    # -------------------------
    # Academic Digital Twin (Future Simulation)
    # -------------------------
    future_score_if_more_study = predicted_score + 5
    future_score_if_less_sleep = predicted_score - 7

    # -------------------------
    # Save to Database
    # -------------------------
    prediction_data = {
        "study_hours": study_hours,
        "attendance": attendance,
        "sleep_hours": sleep_hours,
        "predicted_score": predicted_score,
        "risk_level": risk,
        "burnout_level": burnout,
        "productivity_score": productivity_score,
        "future_score_if_more_study": future_score_if_more_study,
        "future_score_if_less_sleep": future_score_if_less_sleep
    }

    mongo.db.predictions.insert_one(prediction_data)

    # -------------------------
    # Response
    # -------------------------
    return jsonify({
        "predicted_score": predicted_score,
        "risk_level": risk,
        "burnout_level": burnout,
        "productivity_score": productivity_score,
        "digital_twin": {
            "if_study_more": future_score_if_more_study,
            "if_sleep_less": future_score_if_less_sleep
        }
    })


# -------------------------
# RUN SERVER
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)