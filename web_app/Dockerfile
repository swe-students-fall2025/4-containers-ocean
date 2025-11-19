FROM python:3.10-slim

# install small system deps (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# copy only requirements first to cache pip install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV MONGO_URI=mongodb://mongodb:27017/emotiondb
ENV UPLOAD_DIR=/data/uploads

# create uploads dir in container (mounted to named volume)
RUN mkdir -p /data/uploads

VOLUME [ "/data/uploads" ]

EXPOSE 5000
CMD ["python", "app.py"]
