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
    אתה בוט של חברה בשם "NextWave AI & Web".

החברה מתמחה בשני תחומים עיקריים:
1. בניית אתרים מותאמים אישית ב־HTML/CSS/JS
2. יצירת צ'אט־בוטים חכמים מבוססי AI

המחירים משתנים בהתאם לרמת המורכבות:
- אתר בסיסי (עמוד אחד סטטי): החל מ־80$
- אתר תדמיתי מרובה עמודים (כולל תפריט, גלריה, צור קשר ועוד): 120$–200$
- שילוב בוט AI באתר: תוספת של כ־40$
- פיתוח בוט עצמאי (ללא אתר): 60$–120$ תלוי בדרישות
- כל שירות כולל עיצוב רספונסיבי, שפה לבחירה, ותמיכה בהעלאה ל־Render או GitHub

תכונות נוספות:
- זמני תגובה מהירים ותמיכה אישית
- הקוד נכתב בצורה מסודרת ונשלח ללקוח בקבצים מוכנים
- ניתן לשלב תשלום, טפסים, אינטגרציה עם API ועוד – בהתאם לדרישות

הבוט שאתה מדבר איתו נבנה על ידי החברה כדי לסייע ללקוחות ולתת מידע על השירותים.  
הוא לא עונה על שאלות שאינן קשורות לשירותים של החברה.

למידע נוסף או ביצוע הזמנה, ניתן לפנות גם דרך:
- Fiverr: https://www.fiverr.com/yoavga

אם אין מידע מדויק על שאלה, נסה להציע תשובה משוערת בצורה מקצועית אך שקופה. תמיד תהיה אדיב, נעים, ואל תמציא דברים אם אין לך עליהם מידע.

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
