from flask import Flask, jsonify, render_template
import json
import os

app = Flask(__name__)

SCORES_FILE = os.path.join(os.path.dirname(__file__), "scores.json")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scores.json")
def get_scores():
    try:
        with open(SCORES_FILE, "r") as f:
            scores = json.load(f)
        return jsonify(scores)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
