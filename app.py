from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# טוקנים מהסביבה
TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY")
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
TOGETHER_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"

business_info = (
    "Our services and starting prices are:\n"
    "- Website Only: Basic $80, Standard $150, Pro $250\n"
    "- Bot Only (No AI): Basic $60, Standard $100, Pro $160\n"
    "- Bot with AI: Basic $120, Standard $200, Pro $300\n"
    "- Website + Bot: Basic $160, Standard $280, Pro $420\n"
    "- Website + AI Bot: Basic $200, Standard $340, Pro $500\n\n"
    "All services include setup, basic support, and responsive design.\n"
    "For AI bots, clients provide their own API key.\n\n"
    "For contact, email and Fiverr links are available at the bottom of the main page.answer what the usre asked for and not more"
)


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
