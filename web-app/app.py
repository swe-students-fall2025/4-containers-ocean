from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import os
import datetime

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017/emotiondb")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/data/uploads")

client = MongoClient(MONGO_URI)
db = client["emotiondb"]

audio_queue = db["audio_queue"]
emotion_results = db["emotion_results"]  # collection with ML results


@app.route("/")
def index():
    # Build emotion history from MongoDB for initial render
    emotion_history = {}
    for doc in emotion_results.aggregate(
        [
            {"$sort": {"timestamp": -1}},
            {"$group": {"_id": "$emotion", "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}},
        ]
    ):
        emotion = doc["_id"]
        if emotion:
            emotion_history[emotion] = doc["count"]

    # Find last emotion
    last_doc = emotion_results.find_one(sort=[("timestamp", -1)])
    last_emotion = last_doc.get("emotion") if last_doc else None

    return render_template(
        "index.html",
        emotion_history=emotion_history,
        last_emotion=last_emotion,
    )


@app.route("/upload", methods=["POST"])
def upload():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    file = request.files["audio"]
    filename = file.filename
    filepath = os.path.join(UPLOAD_DIR, filename)

    file.save(filepath)

    audio_queue.insert_one(
        {
            "filename": filename,
            "filepath": filepath,
            "timestamp": datetime.datetime.utcnow(),
            "status": "pending",
        }
    )

    return jsonify({"message": "uploaded", "filename": filename})


@app.route("/history-json")
def history_json():
    """JSON API so the dashboard can auto-refresh."""
    emotion_history_dict = {}

    for doc in emotion_results.aggregate(
        [
            {"$sort": {"timestamp": -1}},
            {"$group": {"_id": "$emotion", "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}},
        ]
    ):
        emotion = doc["_id"]
        if emotion:
            emotion_history_dict[emotion] = doc["count"]

    last_doc = emotion_results.find_one(sort=[("timestamp", -1)])
    last_emotion = last_doc.get("emotion") if last_doc else None

    return jsonify(
        emotion_history=emotion_history_dict,
        last_emotion=last_emotion,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
