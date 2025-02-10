from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import requests
import joblib
# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Mistral API Key
mistral_api_key = "add_ur_created_mistralAI_api_key"
# Replace with your ML model path
ml_mdel = "health_risk_model.pkl"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/questionnaire")
def questionnaire():
    return render_template("questionnaire.html")


@app.route("/submit", methods=["POST"])
def handle_submission():
    # Collect form data
    form_data = {
        "age": request.form.get("age"),
        "gender": request.form.get("gender"),
        "height": request.form.get("height"),
        "weight": request.form.get("weight"),
        "heart_rate": request.form.get("heart-rate"),
        "sleep": request.form.get("sleep"),
        "physical_activity": request.form.get("physical-activity"),
        "water_intake": request.form.get("water-intake"),
        "diet": request.form.getlist("diet"),
        "chronic_conditions": request.form.get("chronic-conditions"),
        "allergies": request.form.get("allergies"),
        "smoking": request.form.get("smoking"),
        "alcohol": request.form.get("alcohol"),
    }

    prompt = f"""
Based on the following user details:
- Age: {form_data['age']}
- Gender: {form_data['gender']}
- Height: {form_data['height']} cm
- Weight: {form_data['weight']} kg
- Heart Rate: {form_data['heart_rate']} bpm
- Sleep: {form_data['sleep']} hours/day
- Physical Activity: {form_data['physical_activity']}
- Water Intake: {form_data['water_intake']} liters/day
- Diet Preferences: {', '.join(form_data['diet']) if form_data['diet'] else 'None'}
- Chronic Conditions: {form_data['chronic_conditions']}
- Allergies: {form_data['allergies']}
- Smoking: {form_data['smoking']}
- Alcohol: {form_data['alcohol']}

Provide unique and accurate personalized health recommendations on the basis of above information
1) Sleep Hours: advice on sleep duration in short in 2-3 bullet points each on a new line.
2) Diet and Water Intake: diet recommendation with required nutrition in short in 2-3 bullet points each on a new line.
3) Exercise/Yoga/Workout: Provide exercise, yoga, or fitness routines that suit the user's needs in short in 2-3 bullet points on a new line.
4) Weight Management: Guidance on maintaining a healthy weight, improving metabolism, and lifestyle changes in understandable words in short in 2-3 bullet points each on a new line.
5)Risk Prediction:Predict the health risks based on the users health data in one single point.
small instruction : give the bullet point as $
"""

    mistral_url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {mistral_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral-large-latest",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 600,
        "temperature": 0.7
    }

    try:
        response = requests.post(mistral_url, headers=headers, json=data)
        response.raise_for_status()

        result = response.json()
        recommendation = result.get("choices")[0].get(
            "message", {}).get("content", "")

        # Format recommendation into categories
        f_recommendation = recommendation.replace("$", "•").strip()

        categories = {
            "sleep": "",
            "diet": "",
            "exercise": "",
            "weight_management": "",
            "risk_prediction": ""
        }

        if f_recommendation:
            lines = f_recommendation.split("\n")
            current_category = None

            for line in lines:
                line = line.strip()
                if "Sleep Hours" in line:
                    current_category = "sleep"
                elif "Diet and Water Intake" in line:
                    current_category = "diet"
                elif "Exercise/Yoga/Workout" in line:
                    current_category = "exercise"
                elif "Weight Management" in line:
                    current_category = "weight_management"
                elif "Risk Prediction" in line:
                    current_category = "risk_prediction"
                elif current_category:
                    categories[current_category] += line + "<br>"

        return render_template(
            "dashboard.html",
            sleep_recommendation=categories["sleep"],
            diet_recommendation=categories["diet"],
            exercise_recommendation=categories["exercise"],
            weight_management_recommendation=categories["weight_management"],
            risk_prediction_recommendation=categories["risk_prediction"]
        )

    except requests.exceptions.HTTPError as e:
        categories = {
            "sleep": "Error: Unable to generate recommendations.",
            "diet": "Error: Unable to generate recommendations.",
            "exercise": "Error: Unable to generate recommendations.",
            "weight_management": "Error: Unable to generate recommendations.",
            "risk_prediction": "Error:Unable to generate recommendations."
        }

        return render_template(
            "dashboard.html",
            sleep_recommendation=categories["sleep"],
            diet_recommendation=categories["diet"],
            exercise_recommendation=categories["exercise"],
            weight_management_recommendation=categories["weight_management"],
            risk_prediction_recommendation=categories["risk_prediction"]
        )


if __name__ == "__main__":
    app.run(debug=True)
