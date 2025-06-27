from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# קבלת טוקן מהסביבה
HUGGINGFACE_API_TOKEN = os.environ.get("HUGGINGFACE_API_TOKEN")
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-alpha"

# מידע מותאם לספרייה
business_info = (
    "אתה בוט של ספרייה בשם 'ספריית גבעתיים'.\n"
    "ענה רק לפי המידע הבא:\n"
    "- שעות פתיחה: ראשון עד חמישי, 8:00 עד 20:00\n"
    "- כתובת: רחוב הרצל 10, גבעתיים\n"
    "- מחיר: הכניסה חופשית\n"
    "- טלפון: 03-1234567\n"
    "אל תענה על שאלות שלא קשורות לספרייה. אם יש משהו שקשור חלקית, תענה בצורה אנושית ונעימה."
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data.get("message", "")

    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": f"{business_info}\n\nשאלה: {user_message}",
        "parameters": {
            "max_new_tokens": 100,
            "return_full_text": False
        }
    }

    try:
        response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        output = response.json()

        # הוצאת התשובה מהתגובה
        if isinstance(output, list) and "generated_text" in output[0]:
            answer = output[0]["generated_text"]
        elif "error" in output:
            answer = f"שגיאה מהמודל: {output['error']}"
        else:
            answer = "לא התקבלה תשובה מהמודל."

        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": f"שגיאה: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)

