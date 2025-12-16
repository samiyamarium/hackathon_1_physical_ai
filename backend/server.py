from flask import Flask, request, jsonify
from chatkit import Chatbot

app = Flask(__name__)

# =========================
# INIT CHATBOT
# =========================
try:
    chatbot = Chatbot()
    print("✅ Chatbot initialized successfully")
except Exception as e:
    print("❌ Chatbot initialization failed:", e)
    chatbot = None

# =========================
# ROUTES
# =========================
@app.route("/chat", methods=["POST"])
def chat():
    if chatbot is None:
        return jsonify({"error": "Chatbot not available"}), 500

    data = request.get_json()
    if not data or "question" not in data:
        return jsonify({"error": "Question not provided"}), 400

    try:
        response = chatbot.ask(data["question"])
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(port=5001, debug=True)
