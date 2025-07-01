from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# טוקנים מהסביבה
HUGGINGFACE_API_TOKEN = os.environ.get("HUGGINGFACE_API_TOKEN")
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-alpha"

TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY")
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
TOGETHER_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"

# מידע עסקי
business_info = (
    "You are a helpful assistant for a company named 'NextWave AI & Web'. "
    "We offer custom website development (starting at $80), AI chatbot building (starting at $100), "
    "e-commerce integration, and more. Response time is fast and support is professional. "
    "You were built by NextWave AI & Web. For pricing and orders visit our Fiverr page: "
    "https://www.fiverr.com/yoavgablinger/build-a-custom-ai-chatbot-in-python-using-your-chosen-api. "
    "Only respond about these services and always be polite and informative."
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

    huggingface_headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
        "Content-Type": "application/json"
    }

    together_headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    huggingface_payload = {
        "inputs": f"{business_info}\n\nQuestion: {user_message}",
        "parameters": {
            "max_new_tokens": 100,
            "return_full_text": False
        }
    }

    together_payload = {
        "model": TOGETHER_MODEL,
        "messages": [
            {"role": "system", "content": business_info},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }

    try:
        response = requests.post(TOGETHER_API_URL, headers=together_headers, json=together_payload)
        response.raise_for_status()
        output = response.json()
        if "choices" in output and output["choices"]:
            answer = output["choices"][0]["message"]["content"].strip()
        else:
            answer = "No answer received from model."
    except Exception as e:
        try:
            response = requests.post(HUGGINGFACE_API_URL, headers=huggingface_headers, json=huggingface_payload)
            response.raise_for_status()
            output = response.json()
            if isinstance(output, list) and "generated_text" in output[0]:
                answer = output[0]["generated_text"]
            elif "error" in output:
                answer = f"Model error: {output['error']}"
            else:
                answer = "No answer received from model."
        except Exception as e2:
            return jsonify({"error": f"Both APIs failed: {str(e)} ; {str(e2)}"}), 500

    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
0.0", port=3000)
