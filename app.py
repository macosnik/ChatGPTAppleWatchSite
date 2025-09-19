from flask import Flask, request, jsonify, render_template_string, send_from_directory
from datetime import datetime
import markdown
from g4f.client import Client
from g4f.Provider import PollinationsAI
import os

app = Flask(__name__)
chat_history = []
client = Client(provider=PollinationsAI)

def load_html():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.route("/", methods=["GET"])
def index():
    chat_history.clear()
    return render_template_string(load_html())

@app.route("/style.css")
def style():
    return send_from_directory(os.getcwd(), "style.css")

@app.route("/script.js")
def script():
    return send_from_directory(os.getcwd(), "script.js")

@app.route("/send", methods=["POST"])
def send():
    data = request.get_json()
    text = (data.get("message") or "").strip()
    if not text:
        return jsonify({"reply_html": ""})

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    chat_history.append({"role": "user", "text": text, "time": timestamp})

    try:
        g4f_messages = []
        for m in chat_history:
            if m["role"] == "user":
                g4f_messages.append({"role": "user", "content": m["text"]})
            else:
                g4f_messages.append({"role": "assistant", "content": m["text"]})

        chat_completion = client.chat.completions.create(
            model="openai-fast",
            messages=g4f_messages,
        )
        pc_reply_raw = chat_completion.choices[0].message.content or ""
        pc_reply_html = markdown.markdown(pc_reply_raw)
    except Exception as e:
        pc_reply_html = f"<i>Ошибка при получении ответа: {e}</i>"

    chat_history.append({"role": "pc", "text": pc_reply_html, "time": timestamp})
    return jsonify({"reply_html": pc_reply_html})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=False)
