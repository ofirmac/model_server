from flask import Flask, jsonify, request
import json
from stable_baselines3 import DQN
import numpy as np
import os

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
    data = request.get_json()
    print(f"data {data}")
    # Extracting and processing the observation from the input data
    # observation_str = data.get("observation")

    observation_str = data.get('observation', '[]')
    print(f"observation_str {observation_str}")
    # try:
    #     # Convert the observation string into a list of floats
    #     observation = json.loads(observation_str)
    # except ValueError:
    #     return jsonify({"error": "Invalid observation format. Must be a list of numbers in string format."}), 400
    
    try:
        observation_list = eval(observation_str)  # Use eval carefully or use json.loads if the input is proper JSON
        formatted_observation = [round(float(num), 2) for num in observation_list]
        
        # Return the formatted observation
        # return jsonify({
        #     'formatted_observation': formatted_observation
        # })
    except (ValueError, SyntaxError) as e:
        return jsonify({
            'error': 'Invalid input format'
        }), 400
    
    model = DQN.load("model/10msteps_19_Oct_24")

    # obs_arg = np.array([[[ 6.44454346e+02, -2.35619450e+00, 0.0, float(observation_str[1])],
    #                     [ 5.21175171e+02, -2.61799157e-01, 0.0,float(observation_str[4])],
    #                     [ 1.84370392e+02,  1.83259571e+00, 0.0, float(observation_str[7])],
    #                     [ 7.80000000e+01,  7.85398185e-01, 0.0, 0.00000000e+00]]])


    obs_arg = np.array([[ 6.4445435e+02,  6.4445435e+02, -2.3561945e+00,  formatted_observation[0]],
                        [ 1.8437039e+02,  5.2117517e+02, -2.6179916e-01,  formatted_observation[1]],
                        [ 5.2117523e+02,  1.8437039e+02,  1.8325957e+00,  formatted_observation[2]],
                        [ 7.8000000e+01,  7.8000000e+01,  7.8539819e-01,  0.0000000e+00]])

    print(formatted_observation[0])
    print(formatted_observation[1])
    print(formatted_observation[2])

    action, _states = model.predict(obs_arg, deterministic=True)

    # Generate the required response format
    response = {
        "_intput": str(obs_arg),  # Mock fixed input string
        "input": str(formatted_observation),  # Return the input as received, converted to a string
        "prediction": str(action)  # Prediction (mock example)
    }
    return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
    # app.run(host='0.0.0.0', port=5000)



# {
#     "observation": "[0.0, 0.5, -0.1, 1.0, 2.5, 3.2, 4.1, 5.7]"
# }
