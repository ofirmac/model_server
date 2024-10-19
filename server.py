from flask import Flask, jsonify, request
import json
from stable_baselines3 import DQN
import numpy as np

app = Flask(__name__)

# Initialize global state or any necessary data
global_state = {"count": 0}

# /reset endpoint to reset the global state
@app.route('/reset', methods=['GET'])
def reset():
    global global_state
    global_state["count"] = 0
    return jsonify({"message": "State has been reset", "state": global_state})

# /predict endpoint to return a prediction (for simplicity, just returning a count-based response)
@app.route('/predict', methods=['POST'])
def predict():
    global global_state
    data = request.json
    print(f"data {data}")
    # Extracting and processing the observation from the input data
    observation_str = data.get("observation")
    print(f"observation_str {observation_str}")
    try:
        # Convert the observation string into a list of floats
        observation = json.loads(observation_str)
    except ValueError:
        return jsonify({"error": "Invalid observation format. Must be a list of numbers in string format."}), 400
    
    model = DQN.load("ofirModel")

    obs_arg = np.array([[[ 6.44454346e+02, -2.35619450e+00,  float(observation_str[1])],
                        [ 5.21175171e+02, -2.61799157e-01, float(observation_str[4])],
                        [ 1.84370392e+02,  1.83259571e+00,  float(observation_str[7])],
                        [ 7.80000000e+01,  7.85398185e-01,  0.00000000e+00]]])
    
    action, _states = model.predict(obs_arg, deterministic=True)

    # Generate the required response format
    response = {
        "_intput": "[0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.\n 0. 0. 0. 0. 1. 3. 0. 0.]",  # Mock fixed input string
        "input": str(observation),  # Return the input as received, converted to a string
        "prediction": str(action)  # Prediction (mock example)
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
