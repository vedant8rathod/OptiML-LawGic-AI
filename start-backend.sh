#!/bin/bash

echo "🚀 Starting LawGic AI Backend..."
echo "=================================="

cd backend

echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

echo "🗄️ Initializing database..."
python3 init_db.py

echo "🔧 Starting FastAPI server..."
echo "📍 Backend will be available at: http://127.0.0.1:8000"
echo "📚 API Documentation at: http://127.0.0.1:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=================================="

python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload