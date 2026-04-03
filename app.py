from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from simulator import predict_trajectories   # <-- NEW IMPORT

app = Flask(__name__)


# MongoDB Atlas connection (replace with your own)
app.config["MONGO_URI"] = "mongodb+srv://adityapatidar1810_db_user:Df8mECWr19ZmIs8O@cluster0.c3ofyk3.mongodb.net/academic_db?retryWrites=true&w=majority"

mongo = PyMongo(app)

# Home Route
@app.route("/")
def home():
    return "AI Study Planner Backend Running"


# -------------------------
# BASIC PREDICTION API
# -------------------------
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    study_hours = data.get("study_hours", 0)
    attendance = data.get("attendance", 0)
    sleep_hours = data.get("sleep_hours", 0)

    predicted_score = (
        (study_hours * 5) +
        (attendance * 0.4) +
        (sleep_hours * 2)
    )

    # Risk Level
    if predicted_score < 50:
        risk = "High"
    elif predicted_score < 75:
        risk = "Medium"
    else:
        risk = "Low"

    # Burnout Detection
    if sleep_hours < 5 and study_hours > 8:
        burnout = "High"
    elif sleep_hours < 6:
        burnout = "Medium"
    else:
        burnout = "Low"

    # Productivity Score
    productivity_score = (study_hours * 10) + (sleep_hours * 5)

    # Save to MongoDB
    mongo.db.students.insert_one({
        "study_hours": study_hours,
        "attendance": attendance,
        "sleep_hours": sleep_hours,
        "predicted_score": predicted_score,
        "risk_level": risk,
        "burnout_level": burnout,
        "productivity_score": productivity_score
    })

    return jsonify({
        "predicted_score": predicted_score,
        "risk_level": risk,
        "burnout_level": burnout,
        "productivity_score": productivity_score
    })


# -------------------------
# ML DIGITAL TWIN SIMULATION
# -------------------------
@app.route("/simulate", methods=["POST"])
def simulate():
    data = request.get_json()

    result = predict_trajectories(data)

    return jsonify(result)


# -------------------------
# BROWSER TEST
# -------------------------
@app.route("/browser-test")
def browser_test():
    return jsonify({
        "message": "Backend working",
        "predict_api": "/predict",
        "simulate_api": "/simulate"
    })


if __name__ == "__main__":
    app.run(debug=True)
