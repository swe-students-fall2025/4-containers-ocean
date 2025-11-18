from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
import datetime
from flask import render_template

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017/emotiondb")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/data/uploads")

client = MongoClient(MONGO_URI)
db = client["emotiondb"]
audio_queue = db["audio_queue"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    file = request.files["audio"]
    filename = file.filename
    filepath = os.path.join(UPLOAD_DIR, filename)

    file.save(filepath)

    audio_queue.insert_one({
        "filename": filename,
        "filepath": filepath,
        "timestamp": datetime.datetime.utcnow(),
        "status": "pending"
    })

    return jsonify({"message": "uploaded", "filename": filename})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
