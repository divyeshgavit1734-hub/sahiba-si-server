import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Sahiba server is running 💜"})

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("message", "").strip()

        if not message:
            return jsonify({"error": "Message is empty"}), 400

        api_key = os.environ.get("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")
        if not api_key:
            return jsonify({"error": "AI key is not configured"}), 500

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
                        "and helpful."
                    )
                },
                {"role": "user", "content": message}
            ]
        )

        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": "AI request failed"}), 500
