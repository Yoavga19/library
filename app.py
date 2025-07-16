from flask import Flask, request, jsonify, render_template
import os
import openai

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
    "For contact, email and Fiverr links are available at the bottom of the main page. Answer what the user asked for and not more."
)

# הגדרות ל־GitHub Models
openai.base_url = ENDPOINT
openai.api_key = GITHUB_TOKEN

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

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

    try:
        chat_completion = openai.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": business_info},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=100
        )
        print(chat_completion)  # לראות בלוג מה חזר
        answer = chat_completion.choices[0].message.content.strip()
        return jsonify({"answer": answer})
    except Exception as e:
        import traceback
        print("---- GITHUB TOKEN:", GITHUB_TOKEN)
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


# בדיקת TOKEN
@app.route("/check-token")
def check_token():
    return jsonify({"token": GITHUB_TOKEN})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
