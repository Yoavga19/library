import requests
from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
ENDPOINT = "https://models.github.ai/inference"
MODEL_NAME = "openai/gpt-4.1"

business_info = (
    "Our services and starting prices are:\n"
    "- Website Only: Basic $80, Standard $150, Pro $250\n"
    "- Bot Only (No AI): Basic $60, Standard $100, Pro $160\n"
    "- Bot with AI: Basic $120, Standard $200, Pro $300\n"
    "- Website + Bot: Basic $160, Standard $280, Pro $420\n"
    "- Website + AI Bot: Basic $200, Standard $340, Pro $500\n\n"
    "All services include setup, basic support, and responsive design.\n"
    "For AI bots, clients provide their own API key.\n\n"
    "Note: I am a developer with some experience (not expert).\n"
    "The website and Fiverr profile linked below are examples of my work.\n\n"
    "Contact:\n"
    "Email: nextwaveaiandweb@gmail.com\n"
    "Fiverr: https://www.fiverr.com/sellers/yoavga/edit\n\n"
    "Answer only what the user asks without adding extra information."
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data.get("message", "")

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": business_info},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }

    try:
        response = requests.post(f"{ENDPOINT}/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        output = response.json()
        answer = output["choices"][0]["message"]["content"].strip()
        return jsonify({"answer": answer})
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


@app.route("/check-token")
def check_token():
    return jsonify({"token": GITHUB_TOKEN})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
