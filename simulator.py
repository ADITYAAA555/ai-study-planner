import pickle
import pandas as pd

def predict_trajectories(student_data):
    """
    Expects student_data dict with: 
    'study_hours', 'attendance', 'difficulty' (1-3), 'prior_knowledge' (0 or 1)
    """
    with open('academic_prediction_model.pkl', 'rb') as file:
        model = pickle.load(file)

    h = student_data.get('study_hours', 0)
    a = student_data.get('attendance', 0)
    d = student_data.get('difficulty', 2) # 1=Easy, 2=Med, 3=Hard
    pk = student_data.get('prior_knowledge', 0) # 0=No, 1=Yes

    def get_prediction(hours, attend):
        # Create DataFrame with all 4 features the model learned
        input_df = pd.DataFrame({
            'weekly_self_study_hours': [hours],
            'attendance_percentage': [attend],
            'subject_difficulty': [d],
            'prior_knowledge': [pk]
        })
        return round(model.predict(input_df)[0], 2)

    return {
        "student": student_data.get('name', 'User'),
        "trajectories": {
            "slacking_off": get_prediction(max(0, h-3), 60),
            "current_track": get_prediction(h, a),
            "optimized_track": get_prediction(h+5, 95)
        }
    }

if __name__ == "__main__":
    # Example: Hard subject, No prior knowledge
    alex_data = {
        "name": "Alex",
        "study_hours": 8,
        "attendance": 75,
        "difficulty": 3,
        "prior_knowledge": 0
    }
    print(predict_trajectories(alex_data))