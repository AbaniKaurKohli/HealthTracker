from flask import Flask, request, jsonify
import pandas as pd
import traceback
import os

app = Flask(__name__)

# Determine the path of the CSV file relative to the script location
csv_file_path = "/app/gym_members_exercise_tracking.csv"

# Load the CSV data
try:
    data = pd.read_csv(csv_file_path)
    print("CSV loaded successfully.")
except Exception as e:
    print(f"Error loading CSV: {str(e)}")
    data = None

# Function to recommend exercises based on BMI
def recommend_exercises(bmi):
    try:
        # Ensure data is loaded
        if data is None:
            raise ValueError("CSV data not loaded correctly.")

        # Print column names for debugging
        print("Columns in dataset:", data.columns)

        # Find the entry closest to the given BMI
        recommended_data = data.loc[(data['BMI'] - bmi).abs().idxmin()]

        # Extract required details for the recommendation
        recommendation = {
            "BMI": float(recommended_data["BMI"]),  # Ensure BMI is a float
            "experience_level": str(recommended_data["Experience_Level"]),  # Ensure experience level is a string
            "calories_burned": float(recommended_data["Calories_Burned"]),  # Ensure calories burned is a float
            "workout_type": str(recommended_data["Workout_Type"]),  # Ensure workout type is a string
            "workout_frequency_days_per_week": int(recommended_data["Workout_Frequency (days/week)"]),  # Ensure it's an int
            "session_duration_hours": float(recommended_data["Session_Duration (hours)"])  # Ensure it's a float
        }

        return recommendation
    except Exception as e:
        print(f"Error in recommend_exercises: {str(e)}")
        return {"error": "An error occurred while processing the request."}

# Health endpoint to allow Kubernetes to check if the service is alive
@app.route('/health', methods=['GET'])
def health():
    try:
        # Check if the service is alive
        if data is not None:
            return 'Healthy', 200  # Service is alive
        else:
            return 'Service Not Ready', 503  # Service is not ready due to missing data
    except Exception as e:
        print(f"Error in /health route: {str(e)}")
        return 'Service Not Ready', 503
    
# Readiness endpoint to let Kubernetes know the service is ready
@app.route('/readiness', methods=['GET'])
def readiness():
    try:
        # You can add a more complex check here if needed, e.g., checking if the data is loaded
        if data is not None:
            return 'Ready', 200  # Returning HTTP 200 OK when the app is ready
        else:
            return 'Service Not Ready', 503  # HTTP 503 if the service is not ready
    except Exception as e:
        print(f"Error in /readiness route: {str(e)}")
        return 'Service Not Ready', 503

@app.route('/recommend_exercises', methods=['POST'])
def recommend():
    try:
        data = request.json
        bmi = data.get('bmi')

        # Validate that BMI is provided
        if bmi is None:
            return jsonify({"error": "BMI is required"}), 400

        # Get recommendations based on BMI
        recommendations = recommend_exercises(bmi)

        return jsonify(recommendations), 200
    except Exception as e:
        # Return detailed error message for debugging
        print(f"Error in /recommend_exercises route: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003, debug=True)
