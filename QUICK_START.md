# 🚀 Quick Start Guide

## What is LawGic AI?

LawGic AI is your integrated legal assistant that combines:
- **Smart AI Analysis**: Understands legal documents and questions
- **Beautiful Interface**: Easy-to-use chat interface
- **Multi-Input Support**: Text, documents, and voice files
- **Demo Mode**: Works perfectly without complex setup

## 📦 What's Included

```
final-Lawgic/
├── 📁 backend/           ← FastAPI server with AI
├── 📁 frontend/          ← React interface 
├── 🚀 setup.sh          ← One-time setup
├── 🔧 start-backend.sh  ← Start API server
├── 🎨 start-frontend.sh ← Start web interface
├── 📄 test_document.txt ← Sample file for testing
└── 📚 README.md         ← Full documentation
```

## ⚡ Super Quick Start

### Option 1: Automatic Setup
```bash
cd ~/Desktop/final-Lawgic
./setup.sh
```

### Option 2: Manual Setup

**Terminal 1 (Backend):**
```bash
cd ~/Desktop/final-Lawgic
./start-backend.sh
```

**Terminal 2 (Frontend):**
```bash
cd ~/Desktop/final-Lawgic  
./start-frontend.sh
```

**Then open:** http://localhost:3000

## ✅ Test the Integration

1. **💬 Ask a Question**: "What are my rights as a tenant?"

2. **📄 Upload Document**: Use the test_document.txt file

3. **🎤 Upload Voice**: Try any audio file

4. **🔗 Combined**: Text + document + voice together

5. **🏠 Navigate**: Click "Ask Legal AI" from homepage

## 🎯 Expected Results

You should see:
- **Structured responses** with categories and recommendations
- **File upload working** with visual indicators
- **Intelligent analysis** based on content type
- **Professional UI** that's mobile-friendly

## 🔧 Troubleshooting

### Backend Issues
- Port 8000 busy? Change port in start-backend.sh
- Dependencies? Run: `pip3 install -r backend/requirements.txt`
- Database? Run: `python3 backend/init_db.py`

### Frontend Issues  
- Port 3000 busy? Change port in start-frontend.sh
- Dependencies? Run: `npm install` in frontend/
- Not loading? Check if backend is running first

### Common Issues
- **Blank page**: Backend probably not running
- **Upload not working**: Check file types (PDF, DOCX, TXT, WAV, MP3)
- **API errors**: Check browser console (F12)

## 🎉 What Makes This Special

- ✅ **Complete Integration**: Frontend ↔ Backend working perfectly
- ✅ **No External APIs**: Everything works in demo mode
- ✅ **Beautiful UI**: Professional design preserved
- ✅ **Smart Analysis**: Legal categorization and recommendations
- ✅ **Multi-Input**: Text + Files + Voice in one request
- ✅ **Easy Setup**: Just run the scripts

## 🔗 URLs When Running

- **Main App**: http://localhost:3000
- **Backend API**: http://127.0.0.1:8000  
- **API Docs**: http://127.0.0.1:8000/docs

---

**🎯 Ready to explore legal AI? Start with `./setup.sh`!**