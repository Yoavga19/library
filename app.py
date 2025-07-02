from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# טוקנים מהסביבה
TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY")
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
TOGETHER_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"

business_info = {
    "style": "ענה בקצרה, רק אם נשאל. אל תנדב מידע שלא התבקש.",
    "about": (
        "הבוט מבוסס על שירותי AI חיצוניים כמו OpenAI או Hugging Face. "
        "לשימוש מלא נדרש מפתח API (API Key) בתשלום מצד הלקוח. "
        "הגרסה באתר פועלת באופן בסיסי ולצורכי הדגמה בלבד."
    ),
    "pricing_note": (
        "למחירון מלא של שירותי בניית אתרים, בוטים עם או בלי AI, ניתן להיכנס לעמוד: "
        "https://webfirst-zk72.onrender.com/services"
    ),
    "contact": {
        "email": "nextwaveaiandweb@gmail.com",
        "fiverr": "https://www.fiverr.com/yoavga"
    },
    "message_if_asked": (
        "💡 שים לב: אני מבוסס על מודל AI חיצוני. לשימוש מלא צריך לספק API Key פרטי. "
        "המחירים והשירותים זמינים כאן: https://webfirst-zk72.onrender.com/services. "
        "לשאלות או הזמנות: yoavwebdev@gmail.com או דרך Fiverr."
    )
}


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

# Catch-all route to allow direct URL access to templates
@app.route('/<path:path>')
def catch_all(path):
    try:
        return render_template(f"{path}.html")
    except:
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
        if "choices" in output:
            return jsonify({"answer": output["choices"][0]["message"]["content"].strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
