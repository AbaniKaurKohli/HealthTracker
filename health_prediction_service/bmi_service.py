from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow all origins

@app.route('/calculate_bmi', methods=['POST'])
def calculate_bmi():
    # Parse input JSON
    data = request.json
    print("Received payload in BMI service:", data)  # Debug log

    try:
        # Extract weight and height, and validate input
        weight = float(data.get('weight', 0))
        height = float(data.get('height', 0))
        
        if weight <= 0 or height <= 0:
            return jsonify({"error": "Invalid weight or height provided"}), 400
        
        # BMI calculation
        bmi = round(weight / (height * height), 2)
        print(f"Calculated BMI: {bmi}")  # Debug log
        
        # Determine BMI category and advice
        if bmi < 18.5:
            advice = "Underweight: Consider consulting a healthcare provider to assess your nutritional status."
        elif 18.5 <= bmi < 24.9:
            advice = "Normal weight: Maintain a balanced diet and regular exercise."
        elif 25 <= bmi < 29.9:
            advice = "Overweight: Aim for a healthy diet and more physical activity."
        else:
            advice = "Obesity: Seek medical advice for weight management strategies."
        
        # Respond with BMI and advice
        return jsonify({
            "bmi": bmi,
            "advice": advice
        })
    
    except (TypeError, ValueError) as e:
        print(f"Error in BMI calculation: {e}")
        return jsonify({"error": "Invalid input provided for BMI calculation"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
