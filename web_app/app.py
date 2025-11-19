from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import os
import datetime

app = Flask(__name__)

TESTING = os.environ.get("TESTING") == "1"

if TESTING:
    # ------------------------------
    # USE FAKE IN-MEMORY COLLECTIONS
    # ------------------------------
    class FakeCollection(list):
        def insert_one(self, doc):
            self.append(doc)

        def aggregate(self, pipeline):
            return self

        def find(self):
            return self

        def find_one(self, sort=None):
            if not self:
                return None
            # return last inserted
            return self[-1]

    audio_queue = FakeCollection()
    emotion_results = FakeCollection()

else:
    # ------------------------------
    # REAL MONGODB (CONTAINERS)
    # ------------------------------
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017/emotiondb")
    client = MongoClient(MONGO_URI)
    db = client["emotiondb"]

    audio_queue = db["audio_queue"]
    emotion_results = db["emotion_results"]


# -------------------------------------------------------
# ROUTES
# -------------------------------------------------------

@app.route("/")
def index():
    emotion_history = {}

    for doc in emotion_results.aggregate([
        {"$sort": {"timestamp": -1}},
        {"$group": {"_id": "$emotion", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}},
    ]):
        emotion = doc["_id"]
        if emotion:
            emotion_history[emotion] = doc["count"]

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

    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/data/uploads")
    filepath = os.path.join(UPLOAD_DIR, filename)
    file.save(filepath)

    audio_queue.insert_one({
        "filename": filename,
        "filepath": filepath,
        "timestamp": datetime.datetime.utcnow(),
        "status": "pending",
    })

    return jsonify({"message": "uploaded", "filename": filename})


@app.route("/history-json")
def history_json():
    emotion_history_dict = {}

    for doc in emotion_results.aggregate([
        {"$sort": {"timestamp": -1}},
        {"$group": {"_id": "$emotion", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}},
    ]):
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
