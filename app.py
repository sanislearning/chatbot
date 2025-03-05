from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

API_KEY = "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"  # Replace with your actual API key
API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Predefined system message to set Lumi's context
SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        "You are Lumi, a supportive companion for people to talk to. "
        "You will listen and provide advice in a clear and concise manner. "
        "Your responses should be friendly, empathetic, and restricted to around two paragraphs in length."
        "If a response can be made in a single paragraph, do so."
    )
}

# Store conversation history
conversation_history = [SYSTEM_MESSAGE]

def chat_with_groq(user_message):
    global conversation_history

    # Append user's message to conversation history
    conversation_history.append({"role": "user", "content": user_message})

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mixtral-8x7b-32768",
        "messages": conversation_history
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        bot_response = response.json()["choices"][0]["message"]["content"]
        
        # Store Lumi's response in conversation history
        conversation_history.append({"role": "assistant", "content": bot_response})
        
        return bot_response
    else:
        return f"Error: {response.status_code}, {response.text}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    if not request.json or "message" not in request.json:
        return jsonify({"error": "Invalid request"}), 400

    user_input = request.json.get("message", "")
    response = chat_with_groq(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
