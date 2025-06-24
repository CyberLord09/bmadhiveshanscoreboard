from flask import Flask, send_from_directory, jsonify, render_template
from flask_cors import CORS
import os
import asyncio
from bot import bot_main

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scores.json")
def get_scores():
    full_path = os.path.join(os.path.dirname(__file__), "scores.json")
    return send_from_directory(directory=os.path.dirname(full_path), path="scores.json", mimetype="application/json")

async def run_flask():
    from werkzeug.serving import make_server

    class ServerThread:
        def __init__(self, app):
            self.server = make_server("0.0.0.0", int(os.environ.get("PORT", 8080)), app)
            self.ctx = app.app_context()
            self.ctx.push()

        def serve_forever(self):
            self.server.serve_forever()

    server = ServerThread(app)
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, server.serve_forever)

async def main():
    await asyncio.gather(
        bot_main(),     # Run Telegram bot
        run_flask(),    # Run Flask server
    )

if __name__ == "__main__":
    asyncio.run(main())
