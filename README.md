

Hugging Face GPT-2 API Proxy

(![Alt text](https://github.com/username/repo-name/blob/main/path/to/image.png?raw=true))


This project is a simple Flask-based proxy server that forwards text generation requests to the Hugging Face Inference API for the GPT-2 model.

Description

This application acts as an intermediary between a client and the Hugging Face API. It exposes a single endpoint (/generate) that accepts a text prompt. It then securely sends this prompt to the Hugging Face API, including the necessary authorization token, and returns the model's response directly to the client. This is useful for abstracting away the direct API call and managing API keys in a centralized server-side environment.

How It Works

Flask Server: The application is built using the Flask web framework to create a simple web server.

Endpoint /generate: It defines a single POST endpoint at /generate.

Request Handling: When a POST request is received at this endpoint, the server extracts the JSON payload. It expects the payload to be an object with an input key (e.g., {"input": "Hello, how are you?"}).

Proxy to Hugging Face: The server then makes a POST request to the Hugging Face API URL for the GPT-2 model (https://api-inference.huggingface.co/models/gpt2).

Authorization: It includes an Authorization header with a Bearer token to authenticate with the Hugging Face API.

Response Forwarding: The JSON response from the Hugging Face API is then forwarded back to the original client.

Error Handling: The application includes basic error handling to catch issues like network problems or bad responses from the Hugging Face API and returns a JSON error message with a 500 status code.

Setup and Usage
1. Prerequisites

Python 3.x

Flask and Requests libraries. You can install them using pip:

Generated bash
pip install Flask requests

2. Configuration

Before running the application, you need to set your Hugging Face API token. In the provided code, the token is hardcoded:

Generated python
API_TOKEN = "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"
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Python
IGNORE_WHEN_COPYING_END

For production use, it is highly recommended to use environment variables instead of hardcoding secrets.

3. Running the Server

To start the Flask development server, simply run the Python file:

Generated bash
python your_file_name.py
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

The server will start, and by default, it will be accessible at http://127.0.0.1:5000.

4. Making a Request

You can interact with the server by sending a POST request to the /generate endpoint. You can use tools like curl or any API client (like Postman).

Example using curl:

Generated bash
curl -X POST http://127.0.0.1:5000/generate \
-H "Content-Type: application/json" \
-d '{"input": "Once upon a time"}'
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Expected Response:

The server will return a JSON object from the Hugging Face API, which is typically an array containing an object with the generated text.

Generated json
[
    {
        "generated_text": "Once upon a time, the world was a place of great beauty and great danger. The world was a place of great danger, and the world was a place of great danger. The world was a place of great danger, and the world was a place of great danger."
    }
]
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Json
IGNORE_WHEN_COPYING_END
Code
Generated python
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# It is recommended to load the API URL and Token from environment variables
# for better security and flexibility.
API_URL = "https://api-inference.huggingface.co/models/gpt2"
API_TOKEN = "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"  # <-- IMPORTANT: Keep this secret!

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

@app.route("/generate", methods=["POST"])
def generate():
    """
    Handles text generation requests by proxying them to the Hugging Face API.
    """
    try:
        data = request.json
        if not data or "input" not in data:
            return jsonify({"error": "Invalid request. 'input' key is required."}), 400
            
        print("📥 Received data:", data)

        hugging_response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": data["input"]},
            timeout=20  # Increased timeout for model inference
        )
        
        print("📡 HuggingFace response status:", hugging_response.status_code)
        
        # Raise an HTTPError for bad responses (4xx or 5xx)
        hugging_response.raise_for_status()
        
        response_json = hugging_response.json()
        print("📤 Response JSON:", response_json)

        return jsonify(response_json)
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error communicating with Hugging Face API: {e}")
        return jsonify({"error": "Could not connect to the text generation service."}), 502
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # For production, use a proper WSGI server like Gunicorn or uWSGI
    app.run(debug=True)
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Python
IGNORE_WHEN_COPYING_END
