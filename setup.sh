#!/bin/bash

echo "🏛️ LawGic AI - Complete Setup"
echo "============================="
echo ""

echo "This script will set up both backend and frontend dependencies."
echo "After setup, you can use start-backend.sh and start-frontend.sh to run the servers."
echo ""

read -p "Continue with setup? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "🚀 Setting up LawGic AI..."
    echo ""
    
    # Backend setup
    echo "📱 Setting up Backend..."
    cd backend
    echo "  📦 Installing Python dependencies..."
    pip3 install -r requirements.txt
    echo "  🗄️ Initializing database..."
    python3 init_db.py
    echo "  ✅ Backend setup complete!"
    echo ""
    
    # Frontend setup
    echo "🎨 Setting up Frontend..."
    cd ../frontend
    echo "  📦 Installing Node.js dependencies..."
    npm install
    echo "  ✅ Frontend setup complete!"
    echo ""
    
    # Make scripts executable
    echo "🔧 Making startup scripts executable..."
    cd ..
    chmod +x start-backend.sh
    chmod +x start-frontend.sh
    chmod +x setup.sh
    
    echo ""
    echo "🎉 Setup Complete!"
    echo "=================="
    echo ""
    echo "To start the application:"
    echo "1. Run ./start-backend.sh (in one terminal)"
    echo "2. Run ./start-frontend.sh (in another terminal)"
    echo "3. Open http://localhost:3000 in your browser"
    echo ""
    echo "📚 Check README.md for more information!"
    
else
    echo "Setup cancelled."
fi