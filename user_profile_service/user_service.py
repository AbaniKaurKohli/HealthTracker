from flask import Flask, request, jsonify
import pandas as pd
import requests

app = Flask(__name__)

# Load user data (replace with actual database or data handling method)
users = []

# Function to calculate BMI
def calculate_bmi(weight, height):
    return round(weight / (height * height), 2)

# Function to get exercise recommendations based on BMI
def recommend_exercises(bmi):
    try:
        recommendations = requests.post("http://exercise-service:5003/recommend_exercises", json={"bmi": bmi}).json()
        if "error" in recommendations:
            raise ValueError("Failed to fetch exercise recommendations")
        return recommendations
    except Exception as e:
        return {"error": str(e)}

# Endpoint to add a user profile
@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        data = request.json
        name = data.get("name")
        age = data.get("age")
        gender = data.get("gender")
        weight = data.get("weight")
        height = data.get("height")

        # Validate input
        if not name or not age or weight <= 0 or height <= 0:
            return jsonify({"error": "Invalid input provided"}), 400
        
        # Calculate BMI
        bmi = calculate_bmi(weight, height)

        # Get exercise recommendations based on BMI
        exercise_recommendations = recommend_exercises(bmi)
        
        # Store user data (you can replace this with actual database logic)
        user_data = {
            "name": name,
            "age": age,
            "gender": gender,
            "weight": weight,
            "height": height,
            "bmi": bmi,
            "exercise_recommendations": exercise_recommendations
        }
        
        users.append(user_data)  # Add user to the list (or save to database)
        
        return jsonify(user_data), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to get all user profiles
@app.route('/get_users', methods=['GET'])
def get_users():
    try:
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to delete a user profile by name
@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    try:
        data = request.json
        name = data.get("name")

        if not name:
            return jsonify({"error": "Name is required to delete profile"}), 400

        # Find and remove the user from the list
        user_to_delete = next((user for user in users if user["name"] == name), None)

        if user_to_delete:
            users.remove(user_to_delete)
            return jsonify({"message": f"User {name} deleted successfully"}), 200
        else:
            return jsonify({"error": f"User with name {name} not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Readiness probe endpoint
@app.route('/readiness', methods=['GET'])
def readiness():
    return jsonify({"status": "ready"}), 200

# Health probe endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
