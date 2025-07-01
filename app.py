from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# קבלת הטוקן מהסביבה
TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY")
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
TOGETHER_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"

# מידע מותאם לעסק
business_info = (
    "You are a chatbot created by the company 'NextWave AI & Web'. "
    "The company specializes in two main services: "
    "1. Custom website development using HTML/CSS/JS. "
    "2. Smart AI chatbot creation using powerful language models. "
    "Pricing varies based on complexity: "
    "- Basic website (single static page): from $80. "
    "- Full business website (multiple pages with menu, gallery, contact, etc.): $120–$200. "
    "- Adding an AI chatbot to a website: +$40. "
    "- Standalone chatbot development (without website): $60–$120 depending on features. "
    "All services include responsive design, language customization, and optional deployment to Render or GitHub. "
    "Extra features available: payment integration, forms, APIs, user dashboards, and more (upon request). "
    "You, as the chatbot, were built by the company to help customers and answer questions about these services. "
    "You should only answer questions related to the services listed above. "
    "If unsure, you may estimate politely, but always stay professional and avoid making up false information. "
    "For orders or more details, users can visit our Fiverr page: https://www.fiverr.com/yoavgablinger. "
    "Be helpful, polite, and clear at all times."
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/services")
def services():
    return render_template("services.html")
    
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
            answer = "No response from the model."

        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
