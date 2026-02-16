# Setup Guide - AI Job Application Assistant

Complete step-by-step instructions for installing, configuring, and testing the application.

## Prerequisites

Before starting, ensure you have the following installed:

- **Python 3.10 or higher** - Check with `python --version`
- **Node.js 16 or higher** - Check with `node --version`
- **npm 8 or higher** - Check with `npm --version`
- **Git** - For version control
- **pip** - Python package manager (usually included with Python)

### Optional but Recommended
- **Virtual Environment Tool** - `venv` (built-in) or `conda`
- **Git client** - For cloning repository
- **cURL or Postman** - For testing API endpoints

---

## Backend Setup

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Create Python Virtual Environment

**On Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal, indicating the virtual environment is active.

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- **FastAPI** (0.100+) - Web framework
- **Uvicorn** (0.24+) - ASGI server
- **pandas** (2.0+) - Data manipulation
- **scikit-learn** (1.3+) - ML algorithms (TF-IDF, similarity metrics)
- **spaCy** (3.7+) - NLP processing
- **pdfplumber** (0.10+) - PDF text extraction
- **requests** - HTTP client for APIs
- **python-dotenv** - Environment variable management
- **pytest** - Testing framework

### 4. Download spaCy NLP Model

The project uses spaCy for Named Entity Recognition (NER). Download the English model:

```bash
python -m spacy download en_core_web_sm
```

This downloads the English language model (~40 MB) used for resume parsing.

**Verify installation:**
```bash
python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('spaCy model loaded successfully')"
```

### 5. Configure Environment Variables (Optional)

For full functionality, configure external API keys:

```bash
# Create .env file
cp .env.example .env
```

**Edit `.env` and add your keys:**

```ini
# Groq API (Free, Recommended)
GROQ_API_KEY=your_groq_api_key_here

# Adzuna Jobs API (Free, Optional)
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key

# Alternative: OpenAI (Optional, requires payment)
OPENAI_API_KEY=your_openai_api_key

# Environment
ENV=development
```

**Getting API Keys:**

- **Groq API** (Free, ~30k tokens/day):
  1. Visit https://console.groq.com
  2. Sign up for free account
  3. Create API key
  4. Add to `.env`

- **Adzuna Jobs API** (Free to use):
  1. Visit https://developer.adzuna.com
  2. Register as developer
  3. Get App ID and Key
  4. Add to `.env`

**Note**: The app works without API keys with fallback responses, but AI features and live job search will be limited.

### 6. Verify Backend Installation

Test that all dependencies are correctly installed:

```bash
# Test imports
python -c "
import fastapi
import pandas
import sklearn
import spacy
import pdfplumber
import requests
print('✓ All dependencies installed successfully')
"
```

### 7. Start Backend Server

```bash
uvicorn main:app --reload --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process [12345]
INFO:     Application startup complete
```

**Test the server:**
```bash
# In a new terminal
curl http://localhost:8000/health
# Response: {"status":"healthy","service":"AI Job Application Assistant"}
```

**Access API Documentation:**
Open browser and visit: http://localhost:8000/docs
- Interactive Swagger UI for all endpoints
- Try out API requests directly in browser

---

## Frontend Setup

### 1. Navigate to Frontend Directory

```bash
cd ai-frontend
```

### 2. Install Node Dependencies

```bash
npm install
```

This installs:
- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Axios** - HTTP client
- **ESLint** - Code quality

**Verify installation:**
```bash
npm --version
node --version
```

### 3. Configure API Endpoint (Optional)

If backend is not on default localhost:8000, edit `src/api/backend.js`:

```javascript
// Change this line if needed
const API_URL = "http://localhost:8000";
```

### 4. Start Development Server

```bash
npm run dev
```

**Expected output:**
```
VITE v4.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  press h + enter to show help
```

**Open in Browser**: http://localhost:5173/

If port 5173 is already in use, Vite will automatically try the next available port.

### 5. Build for Production (Optional)

```bash
npm run build
```

Creates optimized production build in `dist/` directory.

---

## Complete Installation Test

### Test 1: Backend Health Check

```bash
# Terminal 1: Backend running on port 8000
curl -X GET "http://localhost:8000/health"

# Expected response:
# {"status":"healthy","service":"AI Job Application Assistant"}
```

### Test 2: Resume Analysis

**Create a test file `test_resume.txt`:**
```
John Doe
john@example.com | (555) 123-4567
LinkedIn: linkedin.com/in/johndoe

EXPERIENCE
Senior Software Engineer | TechCorp | Jan 2020 - Present
- Developed Python REST APIs using FastAPI
- Built React dashboards with modern UI components
- Deployed AWS infrastructure using Docker & Kubernetes

Junior Developer | StartupXYZ | Jun 2018 - Dec 2019
- Implemented Python backend services
- Worked with PostgreSQL databases

SKILLS
Technical: Python, JavaScript, React, Django, FastAPI, AWS, Docker, SQL, Git
Soft Skills: Problem Solving, Team Leadership, Communication

EDUCATION
B.S. Computer Science | University (2018)
```

**Test with curl:**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "John Doe john@example.com Python React AWS FastAPI Docker",
    "job_description": "Senior Python Developer with React and AWS experience required. Must know FastAPI."
  }'

# Expected response: ATS score (0-100), matched skills, recommendations
```

### Test 3: Frontend Loading

1. Open http://localhost:5173 in browser
2. You should see:
   - AI Job Application Assistant title
   - Sidebar with feature options
   - "Upload Resume" quick-start card
   - Chat interface on the right
3. No console errors should appear

### Test 4: API Endpoint Testing

**Using cURL:**
```bash
# Test interview prep
curl -X POST "http://localhost:8000/interview-prep" \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Python Developer",
    "skills": ["python", "fastapi", "sql"],
    "experience": 3
  }'

# Test salary insights
curl -X POST "http://localhost:8000/salary-insights" \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Senior Software Engineer",
    "location": "India",
    "experience_years": 5,
    "skills": ["python", "aws", "kubernetes"]
  }'
```

**Using Postman:**
1. Install Postman (https://postman.com)
2. Create new HTTP request
3. Set URL: `http://localhost:8000/analyze`
4. Set Method: POST
5. Set Body (JSON):
   ```json
   {
     "resume_text": "Python Developer with 5 years experience",
     "job_description": "Senior Python Engineer required"
   }
   ```
6. Click Send
7. View response in Body tab

---

## Feature Testing Checklist

### Resume Analysis
- [ ] Upload PDF resume (if pdfplumber installed)
- [ ] Paste resume text
- [ ] Enter job description
- [ ] View ATS score and breakdown
- [ ] Check recommended improvements

### Skill Gap Analysis
- [ ] Enter candidate skills (Python, React, AWS)
- [ ] Enter required skills (Python, React, AWS, Kubernetes)
- [ ] View skill gap analysis
- [ ] Check learning prerequisite graph

### Job Matching
- [ ] Enter candidate profile (skills, years experience)
- [ ] Search for jobs (requires Adzuna API key)
- [ ] View matched jobs scored by relevance
- [ ] Check skill match percentage

### Interview Preparation
- [ ] Enter job title (e.g., "Senior Data Scientist")
- [ ] Enter job description
- [ ] View technical and behavioral questions
- [ ] Read answer frameworks

### Salary Negotiation
- [ ] Enter job title and location
- [ ] Enter years of experience
- [ ] View estimated salary range
- [ ] Check skill premium breakdown

### Chat Interface
- [ ] Type career question
- [ ] Get AI response
- [ ] Upload resume file (optional)
- [ ] Continue conversation context

### Cover Letter Generation
- [ ] Enter resume content
- [ ] Enter job description
- [ ] Generate cover letter
- [ ] View multiple variations

---

## Troubleshooting

### Backend Issues

**Error: "Port 8000 already in use"**
```bash
# Change port
uvicorn main:app --reload --port 8001

# Or kill process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -i :8000
kill -9 <PID>
```

**Error: "ModuleNotFoundError: No module named 'spacy'"**
```bash
# Reinstall all dependencies
pip install --upgrade -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

**Error: "spaCy model not found (en_core_web_sm)"**
```bash
python -m spacy download en_core_web_sm
```

**Error: "ValueError in resume_parser.py"**
- Check that resume text is not empty
- Ensure job description is provided
- Verify text encoding is UTF-8

**Error: "API Key not found" (optional, non-fatal)**
- Set `GROQ_API_KEY` in `.env` for AI features
- Set Adzuna credentials for live job search
- App will use fallback/sample data if keys missing

### Frontend Issues

**Error: "Cannot connect to backend"**
```bash
# Verify backend is running
curl http://localhost:8000/health

# Check API URL in src/api/backend.js
# Should be: const API_URL = "http://localhost:8000";

# If backend on different port:
# Edit src/api/backend.js to match backend port
```

**Error: "Blank page or React errors"**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run dev
```

**Error: "Port 5173 already in use"**
- Vite will automatically use next available port
- Check terminal output for actual URL

**Error: "Cannot import styles/components"**
- Ensure you're in `/ai-frontend` directory
- Check that all imports use correct relative paths
- Verify CSS files exist in expected locations

### Common Issues

**Issue: "JSON.parse error" in network tab**
- Backend may have crashed
- Restart backend server: `uvicorn main:app --reload --port 8000`
- Check backend terminal for error messages

**Issue: "Empty results" from job search**
- Adzuna API key may be invalid
- Check `.env` file for correct credentials
- Verify internet connection

**Issue: "Interview questions not generated"**
- Groq API key needed for AI generation
- Without key, app returns template questions
- Get free key from https://console.groq.com

---

## Environment Setup for Different Operating Systems

### Windows PowerShell
```powershell
# Virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Start backend
uvicorn main:app --reload --port 8000
```

### macOS/Linux Bash
```bash
# Virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Start backend
uvicorn main:app --reload --port 8000
```

### Conda (Alternative)
```bash
# Create conda environment
conda create -n job-assistant python=3.12
conda activate job-assistant

# Install from requirements
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Start backend
uvicorn main:app --reload --port 8000
```

---

## Production Deployment

### Backend Deployment

```bash
# Use Gunicorn with Uvicorn workers for production
pip install gunicorn

gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

### Frontend Production Build

```bash
cd ai-frontend

# Create optimized production build
npm run build

# Serve static files (requires `serve` package)
npm install -g serve
serve -s dist -p 3000
```

### Docker Deployment (Optional)

Both backend and frontend can be containerized for deployment on cloud platforms.

---

## Next Steps

1. **Explore Features**: Try all features with sample data
2. **Read Documentation**: Check [DOCUMENTATION.md](DOCUMENTATION.md) for technical details
3. **Review API**: Visit http://localhost:8000/docs for interactive API documentation
4. **Understand Algorithms**: Read algorithm explanations in DOCUMENTATION.md
5. **Customize**: Modify skills database, salary data, or prompts as needed
6. **Deploy**: Follow production deployment section when ready for live use

---

## Support

If you encounter issues:
1. Check troubleshooting section above
2. Review error messages carefully
3. Verify all prerequisites are installed
4. Check that both backend AND frontend are running
5. Review DOCUMENTATION.md for technical details
6. Open an issue on GitHub with error details

---

**Setup Complete!** Your AI Job Application Assistant is now ready to use.
