from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# Sample weather data for different locations
weather_data = {
    "new york": {
        "temperature": "72°F",
        "humidity": "65%",
        "condition": "Partly Cloudy"
    },
    "london": {
        "temperature": "62°F",
        "humidity": "80%",
        "condition": "Rainy"
    },
    "tokyo": {
        "temperature": "78°F",
        "humidity": "70%",
        "condition": "Sunny"
    },
    "sydney": {
        "temperature": "82°F",
        "humidity": "55%",
        "condition": "Clear"
    },
    "paris": {
        "temperature": "68°F",
        "humidity": "75%",
        "condition": "Cloudy"
    }
}

# Default weather data for unknown locations
default_conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy", "Clear", "Stormy"]

@app.route('/weather', methods=['GET'])
def get_weather():
    location = request.args.get('location', '').lower()
    
    if location in weather_data:
        return jsonify(weather_data[location])
    else:
        # Generate random weather data for unknown locations
        return jsonify({
            "temperature": f"{random.randint(50, 90)}°F",
            "humidity": f"{random.randint(30, 90)}%",
            "condition": random.choice(default_conditions)
        })

if __name__ == '__main__':
    print("Starting mock weather API server on http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=True)