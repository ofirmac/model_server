from flask import Flask, jsonify, request
from stable_baselines3 import DQN
import numpy as np
import logging
import os

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize global state or any necessary data
global_state = {"count": 0}
MODEL_PATH = "model/10msteps_19_Oct_24"
model = None  # Start with no model loaded
current_model_path = MODEL_PATH  # Track the currently loaded model path

def load_model(path=MODEL_PATH):
    """
    Load the model if it hasn't been loaded already.
    """
    global model, current_model_path
    if model is None:
        model = DQN.load(path)
        current_model_path = path
        logger.info(f"Model loaded from {path}")
    return model

@app.route('/', methods=['GET'])
def root():
    """
    Default root endpoint that shows a welcome message and current model status.
    """
    status = "loaded" if model is not None else "not loaded"
    logger.info("State has been reset")
    return jsonify({
        "message": "Welcome to the prediction server!",
        "status": status,
        "current_model_path": current_model_path
    })

@app.route('/reset', methods=['GET'])
def reset_state():
    """
    Reset the global state count to zero.
    """
    global global_state
    global_state["count"] = 0
    return jsonify({"message": "State has been reset", "state": global_state})

@app.route('/predict', methods=['POST'])
def predict():
    """
    Generate a prediction based on the observation provided in the request.
    """
    global global_state

    # Ensure the model is loaded
    current_model = load_model()

    try:
        # Get observation from the request JSON
        data = request.get_json()
        observation_list = data.get("observation")

        # Validate that the observation is a list
        if not isinstance(observation_list, list):
            raise ValueError("Observation should be a list.")

        formatted_observation = [round(float(num), 2) for num in observation_list]
        logger.info(f"Received observation: {formatted_observation}")

    except (ValueError, TypeError):
        logger.error("Invalid observation format", exc_info=True)
        return jsonify({"error": "Invalid observation format. Expected a list of numbers."}), 400

    # Prepare observation array for model input
    obs_arg = np.array([
        [6.4445435e+02, 6.4445435e+02, -2.3561945e+00, formatted_observation[0]],
        [1.8437039e+02, 5.2117517e+02, -2.6179916e-01, formatted_observation[1]],
        [5.2117523e+02, 1.8437039e+02, 1.8325957e+00, formatted_observation[2]],
        [7.8000000e+01, 7.8000000e+01, 7.8539819e-01, 0.0000000e+00]
    ])

    # Generate prediction from the model
    action, _states = current_model.predict(obs_arg, deterministic=True)

     # Log the prediction
    logger.info(f"Generated prediction: {action} for observation: {obs_arg.tolist()}")

    # Structure the response data
    response = {
        "input_observation": formatted_observation,
        "input_array": obs_arg.tolist(),
        "prediction": int(action)  # Ensure action is JSON serializable
    }
    return jsonify(response)

@app.route('/load_model', methods=['POST'])
def reload_model():
    """
    Load a new model from a specified path if provided, or reload the default.
    """
    global model, current_model_path
    data = request.get_json()
    new_path = data.get("path", MODEL_PATH)

    # Load the model only if it is a different path or model is None
    if model is None or new_path != current_model_path:
        model = DQN.load(new_path)
        current_model_path = new_path
        message = f"Model loaded from {new_path}"
        logger.info(message)
    else:
        message = "The specified model is already loaded."
        logger.info(message)

    return jsonify({"message": message, "current_model_path": current_model_path})

@app.route('/model_status', methods=['GET'])
def model_status():
    """
    Endpoint that shows the currently loaded model path and its status.
    """
    status = "loaded" if model is not None else "not loaded"
    return jsonify({
        "status": status,
        "current_model_path": current_model_path
    })

if __name__ == '__main__':
    load_model()  # Load the default model at startup
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
