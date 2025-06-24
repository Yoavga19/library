from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# המידע שאתה רוצה שהבוט ישתמש בו
business_info = (
    "אתה בוט של ספרייה בשם 'ספריית גבעתיים'.\n"
    "ענה רק לפי המידע הבא:\n"
    "- שעות פתיחה: ראשון עד חמישי, 8:00 עד 20:00\n"
    "- כתובת: רחוב הרצל 10, גבעתיים\n"
    "- מחיר: הכניסה חופשית\n"
    "- טלפון: 03-1234567\n"
    "אל תענה על שאלות שלא קשורות לספרייה אבל אם יש משהו שקשור חלקית אתה יכול על תענה אותו דבר כל  הזמן ותהיה יותר אנושי, תענה גן על שאלות יותר ספציפיות הקשורות לספרייה. אם אין לך מידע על שאלה מסויימת בנוגע לספרייה אתה יכול להשלים לפי מה שנראה לך נכון '."
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data.get("message", "")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model":
        "openai/gpt-3.5-turbo",  # מודל שיודע עברית טוב
        "messages": [{
            "role": "system",
            "content": business_info
        }, {
            "role": "user",
            "content": user_message
        }]
    }

    try:
        response = requests.post(OPENROUTER_API_URL,
                                 headers=headers,
                                 json=payload)
        response.raise_for_status()
        answer = response.json()["choices"][0]["message"]["content"]
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
