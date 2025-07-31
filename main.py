from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
# Define Ollama endpoint and model (assuming Ollama provides a REST API endpoint for the model)
OLLAMA_API_URL = "http://localhost:11434/api/generate"  # Example, adjust based on Ollama's actual endpoint.
OLLAMA_MODEL = "mistral"  # Change this based on the actual model you're using.


# POST route to interact with Ollama
@app.route('/generate', methods=['POST'])
def generate():
    try:
        prompt = request.json.get('prompt')
        if not prompt:
            return jsonify({"error": "No prompt provided!"}), 400
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False  # Tell Ollama not to stream the response
        }
        response = requests.post(OLLAMA_API_URL, json=payload)
        if response.status_code != 200:
            return jsonify({"error": "Error contacting Ollama API", "details": response.text}), 500
        result = response.json()
        return jsonify({"response": result.get('response', '')})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Run the Flask server
    app.run(debug=True, host='0.0.0.0', port=5000)
