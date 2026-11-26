
import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "Sahiba server is running 💜",
        "chat_endpoint": "/chat",
        "method": "POST"
    }), 200


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True) or {}
        message = str(data.get("message", "")).strip()

        if not message:
            return jsonify({"error": "Message is empty"}), 400

        # Read the key from Render Environment Variables
        api_key = os.environ.get("GROQ_API_KEY")

        if not api_key:
            logging.error("GROQ_API_KEY is missing")
            return jsonify({"error": "AI service is not configured"}), 500

        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Sahiba, a personal AI assistant. "
                        "You are gentle, intelligent, polite, caring, "
                        "confident, and natural. Speak conversationally. "
                        "Never call the user Ma'am. Keep answers clear "
                        "and helpful. You are a voice assistant, so avoid "
                        "unnecessarily long answers."
                    )
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            temperature=0.7,
            max_tokens=500
        )

        reply = response.choices[0].message.content

        if not reply:
            return jsonify({"error": "AI returned an empty response"}), 502

        return jsonify({"reply": reply}), 200

    except Exception:
        logging.exception("Sahiba AI request failed")
        return jsonify({
            "error": "AI request failed. Check server logs."
        }), 500
