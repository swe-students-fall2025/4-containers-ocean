#!/bin/bash
set -e

echo "🚀 Stopping old containers..."
docker compose down || true

echo "🔨 Rebuilding containers..."
docker compose build --no-cache

echo "📦 Starting containers..."
docker compose up -d mongodb web-app

echo "⏳ Waiting for MongoDB to start..."
sleep 5

WEB_CONTAINER="4-containers-ocean-web-app-1"

echo "🐳 Installing test dependencies in container..."
docker exec -i $WEB_CONTAINER pip install -r /app/requirements-test.txt

echo "🧪 Running tests inside $WEB_CONTAINER..."
docker exec -i $WEB_CONTAINER pytest -v

echo "✅ Done!"
