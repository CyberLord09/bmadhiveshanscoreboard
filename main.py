from flask import Flask, send_from_directory, jsonify, render_template
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scores.json")
def get_scores():
    return send_from_directory(directory=".", path="scores.json", mimetype="application/json")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
