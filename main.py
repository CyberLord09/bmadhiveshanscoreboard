from flask import Flask, send_from_directory, render_template
from flask_cors import CORS
import os
import threading
import asyncio
from bot import main as bot_main

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scores.json")
def get_scores():
    full_path = os.path.join(os.path.dirname(__file__), "scores.json")
    return send_from_directory(directory=os.path.dirname(full_path), path="scores.json", mimetype="application/json")

def run_bot():
    asyncio.run(bot_main())

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
