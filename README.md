# 🎤 Emotion Detection System

![ML Client CI](https://img.shields.io/badge/ML%20Client%20CI-Passing-brightgreen)
![Web App CI](https://img.shields.io/badge/Web%20App%20CI-Passing-brightgreen)

## Project Overview

This project captures **microphone audio recordings**, performs **emotion classification**, stores the results in MongoDB, and displays them on a real-time updating dashboard!

The system runs as **3 coordinated containers** controlled by Docker Compose:

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
       │                   MongoDB                       │
       │ - Stores filename, mean_f0, mean_rms, emotion   │
       │ - Queried by web app for live dashboard         │
       └─────────────────────────────────────────────────┘
```
## Team Members

| Name            | GitHub                                                              |
| --------------- | ------------------------------------------------------------------  |
| (Jayyuan)       | [https://github.com/qiexian-mf](https://github.com/qiexian-mf)      |
| (Harrison Coon) |   [https://github.com/hoc2006-code](https://github.com/hoc2006-code)|
| Jaylon McDuffie | [https://github.com/jm9908](https://github.com/jm9908)              |
| (Sam Murshed)   | [https://github.com/SamMurshed](https://github.com/SamMurshed)      |
---

# Running the Project

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

Visit: **[http://localhost:5050](http://localhost:5050)**

From here, you can:

* Click **Start Recording**
* Record 3 seconds of audio
* View live emotion classification results
* See the latest emotion + emoji
* Watch the table auto-refresh every 5 seconds

---

# Testing

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

# Continuous Integration (CI)

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

# Database Setup (MongoDB)

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

---

# Environment Variables

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
