
from flask import Flask, request, jsonify
import json
import secrets

app = Flask(__name__)

# Load API keys
with open("Task_2/api_keys.json", "r") as file:
    API_KEYS = json.load(file)


@app.route("/process", methods=["POST"])
def process_text():

    # Get API key from request header
    api_key = request.headers.get("X-API-Key")

    # Validate API key
    if not api_key or not any(
        secrets.compare_digest(api_key, key)
        for key in API_KEYS.values()
    ):
        return jsonify({"error": "Invalid or missing API key"}), 401

    # Read JSON input
    data = request.get_json(silent=True)

    if not data or not isinstance(data.get("text"), str) or not data["text"].strip():
        return jsonify({"error": "Valid text is required"}), 400

    # Process text
    processed_text = data["text"].upper()

    return jsonify({
        "message": "Text processed successfully",
        "original_text": data["text"],
        "processed_text": processed_text
    }), 200


if __name__ == "__main__":
    app.run(port=5001, debug=True)