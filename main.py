from flask import Flask, send_from_directory, jsonify, render_template
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # ✅ This enables CORS for all routes

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scores.json")
def get_scores():
    full_path = os.path.join(os.path.dirname(__file__), "scores.json")
    return send_from_directory(directory=os.path.dirname(full_path), path="scores.json", mimetype="application/json")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
