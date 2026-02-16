# ⚡ Quick Start Guide

Get the AI Job Application Assistant running in 5 minutes!

---

## 🎯 Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.10+ installed → Check: `python --version`
- ✅ Node.js 16+ installed → Check: `node --version`
- ✅ pip installed → Check: `pip --version`
- ✅ npm installed → Check: `npm --version`

---

## 🚀 Installation (5 minutes)

### Step 1: Backend Setup (2 minutes)

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Download NLP model
python -m spacy download en_core_web_sm

# Setup environment
cp .env.example .env

# Start server
uvicorn main:app --reload --port 8000
```

✅ Backend running at: **http://localhost:8000**

---

### Step 2: Frontend Setup (2 minutes)

Open a **new terminal**:

```bash
# Navigate to frontend
cd ai-frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

✅ Frontend running at: **http://localhost:5173**

---

## 🔑 API Keys (Optional - For Full Features)

### Get Free API Keys:

1. **Groq API** (for AI features)
   - Visit: https://console.groq.com
   - Sign up → Create API Key
   - Add to `backend/.env`: `GROQ_API_KEY=your_key_here`

2. **Adzuna Jobs API** (for live job search)
   - Visit: https://developer.adzuna.com
   - Register → Get credentials
   - Add to `backend/.env`:
     ```
     ADZUNA_APP_ID=your_app_id
     ADZUNA_APP_KEY=your_app_key
     ```

> 💡 App works without keys but with limited features

---

## ✅ Test Installation

### Test 1: Backend Health
```bash
curl http://localhost:8000/health
```
**Expected**: `{"status":"healthy","service":"AI Job Application Assistant"}`

### Test 2: Run Algorithm Tests
```bash
cd backend
python test_algorithms.py
```
**Expected**: All tests pass with ✓ marks

### Test 3: Open Frontend
Visit: **http://localhost:5173**

**Expected**: See the application homepage

---

## 🎨 Quick Demo

1. **Upload Resume**
   - Click "Resume Analysis" tab
   - Upload a PDF resume
   - Get ATS score and feedback

2. **Search Jobs**
   - Click "Job Search" tab
   - Search for "Python Developer" in "Bangalore"
   - See live job listings

3. **Salary Insights**
   - Click "Salary Negotiation" tab
   - Enter job details
   - Get salary range and advice

---

## ❌ Common Issues

### Issue: `ModuleNotFoundError: No module named 'spacy'`
**Fix**: Install dependencies again
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Issue: `Port 8000 already in use`
**Fix**: Kill existing process
```bash
# Windows
Get-Process -Name "python" | Stop-Process -Force

# Linux/Mac
kill $(lsof -t -i:8000)
```

### Issue: Frontend shows "API Error"
**Fix**: Ensure backend is running on port 8000
```bash
curl http://localhost:8000/health
```

---

## 📁 Project Structure

```
job_application_assistant/
├── backend/           # FastAPI backend
│   ├── main.py       # Main application
│   ├── services/     # Algorithm modules
│   └── .env         # API keys (create this)
├── ai-frontend/      # React frontend
│   └── src/          # Source code
└── README.md         # Full documentation
```

---

## 🎓 Next Steps

1. ✅ **Read Full Docs**: See [README.md](README.md) for complete features
2. ✅ **Understand Algorithms**: Check [ENGINEERING_DOCUMENTATION.md](ENGINEERING_DOCUMENTATION.md)
3. ✅ **Test Features**: Try all 8 features (Resume, Jobs, Salary, etc.)
4. ✅ **Customize**: Modify prompts or add new features

---

## 💡 Pro Tips

- **Use Groq API** (not OpenAI) - It's faster and free
- **Get Adzuna keys** - Essential for live job data
- **Keep servers running** - Use separate terminals for backend/frontend
- **Check logs** - Terminal shows debugging info

---

## 📞 Need Help?

- 📖 **Full Docs**: [README.md](README.md)
- 🔬 **Algorithms**: [ENGINEERING_DOCUMENTATION.md](ENGINEERING_DOCUMENTATION.md)
- 🐛 **Issues**: Check terminal output for error messages
- 📝 **API Docs**: http://localhost:8000/docs (when backend running)

---

**Ready to code! Happy job hunting! 🎉**
