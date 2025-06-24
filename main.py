from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import os
import asyncio
import threading
from bot import bot_main

app = Flask(__name__)
CORS(app)

@app.route("/scores.json")
def get_scores():
    full_path = os.path.join(os.path.dirname(__file__), "scores.json")
    return send_from_directory(directory=os.path.dirname(full_path), path="scores.json", mimetype="application/json")

def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(bot_main())
    loop.run_forever()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
