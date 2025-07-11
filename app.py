from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/gpt2"
API_TOKEN = "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"

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.json
        print("📥 Received data:", data)

        hugging_response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": data["input"]},
            timeout=10
        )
        
        print("📡 HuggingFace response status:", hugging_response.status_code)
        print("📤 Response JSON:", hugging_response.json())

        hugging_response.raise_for_status()
        return jsonify(hugging_response.json())
        
    except Exception as e:
        print("❌ Flask server error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
