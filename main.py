import asyncio
from flask import Flask, send_from_directory
from flask_cors import CORS
from hypercorn.asyncio import serve
from hypercorn.config import Config
from bot import bot_main

app = Flask(__name__)
CORS(app)

@app.route("/scores.json")
def get_scores():
    from os.path import dirname, join
    return send_from_directory(directory=dirname(__file__), path="scores.json", mimetype="application/json")

async def run_flask():
    config = Config()
    config.bind = ["0.0.0.0:8080"]
    await serve(app, config)

async def main():
    await asyncio.gather(
        run_flask(),
        bot_main()
    )

if __name__ == "__main__":
    asyncio.run(main())
