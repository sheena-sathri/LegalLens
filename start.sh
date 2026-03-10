#!/bin/bash
echo "Starting LegalLens..."
mkdir -p data/chroma_db data/sample_contracts data/playbooks

pkill -f "uvicorn main:app" 2>/dev/null
pkill -f "vite" 2>/dev/null
sleep 1

echo "Starting API server on port 8001..."
uvicorn main:app --host 0.0.0.0 --port 8001 &
API_PID=$!
sleep 3

echo "Starting React UI on port 5000..."
npx vite --host 0.0.0.0 --port 5000 &
VITE_PID=$!
sleep 2

echo "LegalLens is running!"
echo "   API: http://localhost:8001/docs"
echo "   UI:  http://localhost:5000"

wait $API_PID $VITE_PID
