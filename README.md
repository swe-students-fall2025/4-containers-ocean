---

# 🎤 Emotion Detection System — Containerized Multi-Service App

![ML Client CI](https://img.shields.io/badge/ML%20Client%20CI-Passing-brightgreen)
![Web App CI](https://img.shields.io/badge/Web%20App%20CI-Passing-brightgreen)

## 📌 Project Overview

This project is a fully containerized, multi-service system built using **Docker**, **Flask**, **MongoDB**, and a custom **machine-learning client**.
It captures **microphone audio recordings**, performs **emotion classification**, stores the results in MongoDB, and displays them on a real-time updating dashboard.

The system runs as **three coordinated containers** controlled by Docker Compose:

1. **Machine Learning Client**

   * Listens for new audio files
   * Extracts acoustic features (f0, RMS)
   * Classifies emotions (Happy, Sad, Neutral, Excited)
   * Stores analysis results in MongoDB

2. **Flask Web App**

   * Records audio via browser
   * Sends audio to shared storage
   * Displays results & live dashboard
   * Auto-refreshes emotion history

3. **MongoDB Database**

   * Stores every recording’s metadata, timestamps, and predicted emotion

---

## 👥 Team Members

| Name            | GitHub                                                             |
| --------------- | ------------------------------------------------------------------ |
| (insert)   | [https://github.com/](https://github.com/)     |
| (insert)   | [https://github.com/](https://github.com/)       |
| Jaylon McDuffie | [https://github.com/jm9908](https://github.com/jm9908)             |
| (insert)    | [https://github.com/](https://github.com/)       |
---

# 🧱 System Architecture

```
┌─────────────────────────────┐      ┌──────────────────────────────┐
│     Flask Web App           │      │      ML Client               │
│  - Audio recording UI       │      │  - Watches for new audio     │
│  - Uploads .webm            │─────▶│  - Extracts features         │
│  - Dashboard of results     │◀─────│  - Predicts emotion          │
└─────────────┬───────────────┘      │  - Writes to MongoDB         │
              │                      └─────────────┬────────────────┘
              │                                    │
              ▼                                    ▼
       ┌─────────────────────────────────────────────────┐
       │                   MongoDB                        │
       │ - Stores filename, mean_f0, mean_rms, emotion   │
       │ - Queried by web app for live dashboard         │
       └─────────────────────────────────────────────────┘
```

---

# 🐳 Running the Project

## **1. Install Dependencies**

Make sure you have:

* Docker
* Docker Compose
* Python 3.10+ (for linting/tests only)

---

## **2. Start All Containers**

```bash
docker compose up --build
```

This will launch:

* `emotion_web` — Flask server
* `emotion_ml` — Machine Learning container
* `emotion_mongodb` — MongoDB

When running successfully:

* Web app → [http://localhost:5050](http://localhost:5050)
* MongoDB exposed on → 27017

---

## **3. View the Dashboard**

Visit:

👉 **[http://localhost:5050](http://localhost:5050)**

From here, you can:

* Click **Start Recording**
* Record 3 seconds of audio
* View live emotion classification results
* See the latest emotion + emoji
* Watch the table auto-refresh every 5 seconds

---

# 📁 Repository Structure

```
4-containers-ocean/
│
├── machine-learning-client/
│   ├── ml_client.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests/
│
├── web-app/
│   ├── app.py
│   ├── templates/
│   │   └── index.html
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests/
│
├── docker-compose.yml
├── run_tests.sh
├── README.md
└── .github/
    └── workflows/
        ├── ml-client-ci.yml
        └── web-app-ci.yml
```

---

# 🧪 Testing

## **Run all tests locally**

```bash
export PYTHONPATH=$PWD
export TESTING=1
pytest -v
```

## **Run tests inside Docker**

A helper script is included:

```bash
./run_tests.sh
```

This script:

* Stops old containers
* Rebuilds everything
* Runs CI tests **inside the web-app container**
* Prints results

---

# 🚀 Continuous Integration (CI)

Two GitHub Actions workflows run automatically:

### `ml-client-ci.yml`

* Lints ML client code using **black** & **pylint**
* Runs `pytest` for ML unit tests
* Reported with a badge in the README

### `web-app-ci.yml`

* Lints Flask server
* Runs Flask unit tests
* Ensures formatting & PEP8 compliance

CI triggers **on pull request merge to main**.

---

# 🗃️ Database Setup (MongoDB)

MongoDB runs via Docker using:

```yml
mongodb:
  image: mongo:6.0
  ports:
    - "27017:27017"
  volumes:
    - mongo_data:/data/db
```

No extra configuration is needed.

If you want to inspect data:

```bash
docker exec -it emotion_mongodb mongosh

use emotiondb
db.emotion_results.find().pretty()
```

---

# 🔐 Environment Variables

Both services use environment variables from docker-compose:

### Web App:

```
MONGO_URI=mongodb://mongodb:27017/emotiondb
UPLOAD_DIR=/data/uploads
```

### ML Client:

```
MONGO_URI=mongodb://mongodb:27017/emotiondb
AUDIO_DIR=/data/uploads
```

A template for secrets should include:

```
.env.example
```

But nothing secret is required for this project.

---

# 🎨 Features Added

### ✔ Audio Recording via Browser

### ✔ Shared Docker Volume for Audio Transfer

### ✔ ML Feature Extraction (f0, RMS)

### ✔ Emotion Classifier with Weighted Rules

### ✔ MongoDB Storage

### ✔ Real-Time Auto-Updating Dashboard

### ✔ Emoji Mapping for Emotions

### ✔ Dark Mode Toggle

### ✔ Last Emotion Card

### ✔ Fully Containerized System

### ✔ CI Workflows for Both Subsystems

### ✔ Unit Tests for ML + Web App

### ✔ 80%+ Code Coverage Achieved

---
