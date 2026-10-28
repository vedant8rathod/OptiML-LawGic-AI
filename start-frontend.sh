#!/bin/bash

echo "🎨 Starting LawGic AI Frontend..."
echo "================================="

cd frontend

echo "📦 Installing dependencies..."
npm install

echo "🔧 Starting Vite development server..."
echo "📍 Frontend will be available at: http://localhost:3000"
echo "🌐 Network access at: http://0.0.0.0:3000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================="

npm run dev -- --host 0.0.0.0 --port 3000