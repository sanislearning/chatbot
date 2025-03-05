from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

API_KEY = "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"  # Replace with your actual API key
API_URL = "https://api.groq.com/openai/v1/chat/completions"  # Corrected URL

@app.route("/")  # Serve the frontend
def home():
    return render_template("index.html")  # Flask will look in "templates" folder

def chat_with_groq(user_message):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": user_message}]
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"

@app.route("/chat", methods=["POST"])
def chat():
    if not request.json or "message" not in request.json:
        return jsonify({"error": "Invalid request"}), 400

    user_input = request.json.get("message", "")
    response = chat_with_groq(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
