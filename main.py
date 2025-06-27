from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

HUGGINGFACE_API_TOKEN = os.environ.get("HUGGINGFACE_API_TOKEN")

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

    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()

        answer = response.json()[0]["generated_text"].split("תשובה:")[-1].strip()
        return jsonify({"answer": answer})

    except requests.exceptions.Timeout:
        print("Error: Request timed out")
        return jsonify({"error": "הבקשה לשרת לקחה יותר מדי זמן, אנא נסה שוב."}), 504

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e} - Response: {response.text}")
        return jsonify({"error": "אירעה שגיאה בשרת, אנא נסה מאוחר יותר."}), 500

    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "אירעה שגיאה לא צפויה, אנא נסה שוב."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
 
