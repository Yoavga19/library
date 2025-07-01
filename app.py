from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# קבלת הטוקן מהסביבה
TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY")
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
TOGETHER_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"  # אפשר לשנות למודל אחר מ together.ai

# מידע מותאם 
business_info = (
     "אתה בוט של עסק בשם 'NextWave AI & Web'.\n"
    "ענה רק לפי המידע הבא:\n"
    "- שירותים: בניית אתרים מותאמים אישית, יצירת בוטים חכמים.\n"
    "- זמני תגובה מהירים ותמיכה מקצועית.\n"
    "- לפרטים והזמנות ניתן לפנות דרך אתר האינטרנט או Fiverr.\n"
    "ענה על שאלות רק לפי המידע הזה והיה אדיב ומקצועי."
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data.get("message", "")

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": TOGETHER_MODEL,
        "messages": [
            {"role": "system", "content": business_info},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }

    try:
        response = requests.post(TOGETHER_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        output = response.json()

        if "choices" in output and output["choices"]:
            answer = output["choices"][0]["message"]["content"].strip()
        else:
            answer = "לא התקבלה תשובה מהמודל."

        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": f"שגיאה: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
