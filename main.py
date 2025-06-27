from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# קח את הטוקן שלך מה־Environment ב־Render
HUGGINGFACE_API_TOKEN = os.environ.get("HUGGINGFACE_API_TOKEN")

# מידע קבוע שהבוט משתמש בו
business_info = (
    "אתה בוט של ספרייה בשם 'ספריית גבעתיים'.\n"
    "ענה רק לפי המידע הבא:\n"
    "- שעות פתיחה: ראשון עד חמישי, 8:00 עד 20:00\n"
    "- כתובת: רחוב הרצל 10, גבעתיים\n"
    "- מחיר: הכניסה חופשית\n"
    "- טלפון: 03-1234567\n"
    "ענה בצורה אנושית ונעימה. אם אין מידע מדויק, נסה להעריך לפי ההיגיון."
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data.get("message", "")

    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
    }

    payload = {
        "inputs": f"שאלה: {user_message}\n{business_info}\nתשובה:"
    }

    response = requests.post(
        "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        answer = response.json()[0]["generated_text"].split("תשובה:")[-1].strip()
        return jsonify({"answer": answer})
    else:
        return jsonify({"error": "שגיאה בקבלת תשובה מהמודל"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
