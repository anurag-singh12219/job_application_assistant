# 🤖 AI Job Application Assistant

> **Challenge 2 Submission**: Advanced algorithms and AI-powered career guidance platform

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.0-61dafb.svg)](https://reactjs.org/)
[![Algorithms](https://img.shields.io/badge/Algorithms-TF--IDF%20%7C%20Fuzzy%20Matching-orange.svg)](#algorithms)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A **production-ready, full-stack application** that combines advanced algorithms with AI to provide comprehensive career guidance. This project demonstrates real engineering work with information retrieval, NLP, and algorithmic problem-solving.

## 📚 Documentation

- **[DOCUMENTATION.md](DOCUMENTATION.md)** - Complete guide with setup, API reference, algorithms, and usage
- **[QUICK_START.md](QUICK_START.md)** - 5-minute installation guide

---

## 🔬 Core Algorithms & Technical Features

### **Algorithm Implementation** (2,000+ Lines of Code)

The project implements multiple sophisticated algorithms for job matching and resume analysis:

1. **TF-IDF Vectorization** - Document similarity using scikit-learn
2. **Fuzzy String Matching** - Jaccard similarity for skill name variations
3. **Multi-Factor Composite Scoring** - Weighted job matching (5 algorithms)
4. **Dependency Graph Resolution** - Learning path generation with prerequisites
5. **Weighted ATS Scoring** - 3-factor resume analysis (TF-IDF 60%, Keywords 25%, Format 15%)
6. **NLP Entity Recognition** - spaCy for resume parsing
7. **Live API Integration** - Adzuna Jobs API (2M+ real job listings)
8. **Linear Regression** - Salary estimation based on experience and location

**See [DOCUMENTATION.md](DOCUMENTATION.md) for detailed algorithm implementation and code examples.**

---

## 📊 Technical Stack

### Backend (Python)
- **Framework**: FastAPI (production-grade async web framework)
- **ML/NLP**: scikit-learn (TF-IDF, cosine similarity), spaCy (entity recognition)
- **PDF Processing**: pdfplumber
- **Data**: pandas, numpy
- **AI**: Groq API (llama-3.1-8b-instant)

### Frontend (React)
- **Framework**: React 18 + Vite
- **HTTP Client**: Axios
- **Styling**: Modern CSS with responsive design

### External APIs
- **Adzuna Jobs API**: 2M+ live job listings with real salaries
- **Groq LLM API**: Strategic text generation (35% of features)

---

## ✨ Features

### 1. 📄 **Resume Analysis** - Advanced ATS Engine
- **TF-IDF Based Scoring**: Weighted algorithm (not just keyword count)
- **80+ Keyword Extraction**: Pattern matching for tech skills, action verbs
- **Format Quality Analysis**: Contact info, sections, quantifiable achievements
- **Detailed Breakdown**: Shows keyword match %, content relevance, format score
- **Smart Recommendations**: Specific action items to improve score

**Algorithm**: O(n*m) time complexity with TF-IDF vectorization

### 2. 🎯 **Skill Gap Analyzer** - Fuzzy Matching
- **Jaccard Similarity**: Handles skill name variations ("react" vs "reactjs")
- **Dependency Graph**: Shows learning prerequisites (e.g., React needs JavaScript)
- **Priority Classification**: Critical vs nice-to-have skills
- **Learning Path Generation**: Topological sort based on dependencies
- **Time Estimation**: Calculates weeks needed to close gaps

**Algorithm**: O(n*m) fuzzy matching + O(n log n) sorting

### 3. 🔍 **Job Matcher** - Multi-Factor Scoring
- **TF-IDF Weighted Matching**: Rare skills get higher weight
- **5-Factor Composite Score**:
  - Skill overlap (30%)
  - TF-IDF weighted (25%)
  - Critical skill importance (20%)
  - Experience alignment (15%)
  - Rarity bonus (10%)
- **Live Job Data**: Adzuna API integration
- **Smart Ranking**: Filters by salary, location, preferences

**Algorithm**: O(n*m*k) where n=jobs, m=skills per job, k=candidate skills

### 4. 💰 **Salary Negotiation** - Market Intelligence
- **Linear Regression Model**: Base salary + experience multiplier
- **34 Role-Location Entries**: US and India salary data
- **Skill Premium Calculator**: Shows % of high-demand skills
- **AI-Powered Insights**: Market trends, negotiation scripts
- **Currency Conversion**: INR ↔ USD with location detection

### 5. 💬 **Interview Preparation** - Role-Specific Questions
- **Scenario-Based Questions**: Realistic technical problems
- **STAR Method**: Structured behavioral questions
- **Answer Frameworks**: Automated guidance generation
- **Company-Specific Tips**: 5-section preparation roadmap

### 6. ✍️ **Cover Letter Generator**
- **Placeholder Detection**: Retry logic to avoid [Position] templates
- **Context-Aware**: Uses resume and job description
- **Professional Formatting**: Multiple styles

### 7. 🌐 **Live Job Search**
- **Adzuna API**: Real listings from 2M+ jobs
- **INR Salaries**: Location-based currency
- **Working Apply Buttons**: Direct application URLs
- **Internship Search**: Dedicated endpoint

### 8. 🗨️ **AI Career Chat**
- **File Upload Support**: Analyze resumes in chat
- **Context-Aware Responses**: Understands career questions
- **Multi-Endpoint**: Handles both text and file inputs

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+ (tested on 3.12)
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd job_application_assistant
   ```

2. **Navigate to backend**
   ```bash
   cd backend
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy NLP model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Configure environment variables**
   ```bash
   # Copy example file
   cp .env.example .env
   
   # Edit .env and add your API keys
   # GROQ_API_KEY=your_groq_api_key_here
   # ADZUNA_APP_ID=your_adzuna_id_here
   # ADZUNA_APP_KEY=your_adzuna_key_here
   ```
   
   **Get API Keys**:
   - **Groq API** (Free): https://console.groq.com
   - **Adzuna Jobs API** (Free): https://developer.adzuna.com
   
   > ⚠️ **Note**: App works without API keys but with limited AI features and no live job data

6. **Run backend server**
   ```bash
   uvicorn main:app --reload --port 8000
   ```
   
   Server will start at: http://localhost:8000

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd ../ai-frontend
   ```

2. **Install Node dependencies**
   ```bash
   npm install
   ```

3. **Configure environment**
   ```bash
   # Copy example file
   cp .env.example .env
   ```

4. **Run development server**
   ```bash
   npm run dev
   ```
   
   App will open at: http://localhost:5173

---

## 🧪 Testing

### Test Core Algorithms
```bash
cd backend
python test_algorithms.py
```

**Expected Output**:
```
✓ Gap Score: 60.0%
✓ Match: 40.0%
✓ Top Match: ML Engineer (73.84%)
✓ ATS Overall Score: 46.35
```

### Test API Health
```bash
curl http://localhost:8000/health
# {"status":"healthy","service":"AI Job Application Assistant"}
```

---

## 📂 Project Structure

```
job_application_assistant/
├── backend/
│   ├── main.py                          # FastAPI application
│   ├── requirements.txt                 # Python dependencies
│   ├── .env.example                     # Environment template
│   ├── test_algorithms.py               # Algorithm tests
│   ├── services/
│   │   ├── ats_engine.py               # TF-IDF ATS scoring (280 lines)
│   │   ├── skill_gap.py                # Fuzzy matching (280 lines)
│   │   ├── job_matcher.py              # Multi-factor scoring (220 lines)
│   │   ├── resume_parser.py            # NLP parsing (130 lines)
│   │   ├── salary_negotiator.py        # Salary estimation (280 lines)
│   │   ├── job_search.py               # Adzuna API (400 lines)
│   │   ├── interview_prep.py           # Question generation (180 lines)
│   │   ├── cover_letter_generator.py   # Cover letter AI (150 lines)
│   │   ├── career_advisor.py           # Feedback system (200 lines)
│   │   └── ai_service.py               # LLM wrapper (190 lines)
│   └── models/
│       └── role_classifier.py          # ML role prediction
├── ai-frontend/
│   ├── src/
│   │   ├── components/                 # React components
│   │   ├── api/backend.js              # API client
│   │   └── App.jsx                     # Main app
│   └── package.json
├── DOCUMENTATION.md                 # Complete technical documentation
├── .gitignore                       # Git ignore rules
└── README.md                        # This file
```

---

## 📊 Key Metrics

| Component | Lines of Code | External Libraries | LLM Usage | Algorithm Type |
|-----------|--------------|-------------------|-----------|----------------|
| ATS Engine | 280 | scikit-learn | 0% | TF-IDF, Cosine Similarity |
| Skill Gap | 280 | None | 0% | Fuzzy Matching, Graph |
| Job Matcher | 220 | pandas, math | 0% | TF-IDF, Composite Scoring |
| Resume Parser | 130 | spaCy, pdfplumber | 0% | NLP, Regex |
| Salary Estimator | 280 | None | 15% | Linear Regression |
| Job Search | 400 | requests | 0% | API Integration |
| Interview Prep | 180 | None | 85% | Prompt Engineering |
| Cover Letter | 150 | None | 85% | Prompt Engineering |

**Total**: ~2,000 lines of code | **Algorithmic Engineering**: 65% | **LLM Wrappers**: 35%

---

## 🎯 API Endpoints

### Resume Analysis
```bash
POST /upload-resume
Content-Type: multipart/form-data

# Returns: ATS score, skills, role prediction, feedback
```

### Job Search
```bash
GET /job-search?keywords=python&location=bangalore&limit=10

# Returns: Live job listings from Adzuna with INR salaries
```

### Salary Insights
```bash
POST /salary-insights
{
  "job_title": "ML Engineer",
  "location": "India",
  "experience_years": 3,
  "skills": ["python", "tensorflow", "aws"]
}

# Returns: Salary range, market insights, negotiation advice
```

### Interview Prep
```bash
POST /interview-prep
{
  "job_title": "Data Scientist",
  "job_description": "...",
  "skills": ["python", "ml", "sql"]
}

# Returns: Technical & behavioral questions with frameworks
```

**Full API documentation**: http://localhost:8000/docs (FastAPI Swagger UI)

---

## 🛠️ Technologies & Algorithms

### Information Retrieval
- **TF-IDF Vectorization**: Term frequency-inverse document frequency for keyword weighting
- **Cosine Similarity**: Document similarity measurement
- **Weighted Scoring**: Multi-factor composite algorithms

### String Algorithms
- **Jaccard Similarity**: Set-based string matching
- **Fuzzy Matching**: Character overlap for skill name variations
- **Normalization**: Handling common variations (e.g., "nodejs" → "node.js")

### Graph Algorithms
- **Dependency Resolution**: Skill prerequisite graphs
- **Topological Sort**: Ordering learning paths by dependencies

### Machine Learning
- **Naive Bayes**: Role classification (sklearn)
- **Linear Regression**: Salary estimation model
- **Feature Extraction**: TF-IDF for text features

### Natural Language Processing
- **Entity Recognition**: spaCy for extracting names, skills, contact info
- **Pattern Matching**: Regex for phone, email, dates
- **Text Extraction**: pdfplumber for PDF parsing

### System Design
- **RESTful API**: FastAPI with async support
- **Error Handling**: Try-except, timeouts, fallbacks
- **Graceful Degradation**: Sample data fallback when APIs fail
- **CORS**: Cross-origin resource sharing configured

---

## 📊 Performance & Complexity

| Algorithm | Time Complexity | Space Complexity | Optimization |
|-----------|----------------|------------------|--------------|
| ATS Scoring | O(n*m) | O(n+m) | TF-IDF vectorization |
| Skill Gap | O(n*m) | O(n+m) | Fuzzy matching with caching |
| Job Matching | O(n*m*k) | O(n) | Pre-computed TF-IDF weights |
| Resume Parsing | O(n*k) | O(n) | Hash map skill lookup |
| Learning Path | O(n log n) | O(n) | Topological sort |

**Legend**: n=document length, m=job description length, k=number of skills

---

## 🚀 Deployment

### Backend (FastAPI)
```bash
# Production server
uvicorn main:app --host 0.0.0.0 --port 8000

# With workers
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend (React)
```bash
# Build for production
npm run build

# Serve static files
npm install -g serve
serve -s dist -p 3000
```

---

## 🤝 Contributing

This is a Challenge 2 submission project. For improvements or issues:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open Pull Request

---

## 📝 License

MIT License - See LICENSE file for details

---

## 👨‍💻 Author

**Anurag Singh**  
Challenge 2 - GenAI Training Program

---

## 🙏 Acknowledgments

- **FastAPI**: Modern Python web framework
- **scikit-learn**: Machine learning algorithms
- **spaCy**: Industrial-strength NLP
- **Adzuna**: Live job data API
- **Groq**: Fast LLM inference

---

## 📚 Learning Resources

If you want to understand the algorithms used:

1. **TF-IDF**: [Wikipedia - TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf)
2. **Cosine Similarity**: [Cosine Similarity Explained](https://en.wikipedia.org/wiki/Cosine_similarity)
3. **Jaccard Index**: [Jaccard Similarity](https://en.wikipedia.org/wiki/Jaccard_index)
4. **NLP with spaCy**: [spaCy Documentation](https://spacy.io/usage/spacy-101)
5. **FastAPI**: [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)

---

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Check [DOCUMENTATION.md](DOCUMENTATION.md) for complete technical details

---

## 🏗️ Project Structure
   ```bash
   uvicorn main:app --reload
   ```
   Backend will run on: `http://127.0.0.1:8000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd ai-frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```
   Frontend will run on: `http://localhost:5173` (or next available port)

### Access the Application

Open your browser and navigate to the frontend URL (usually `http://localhost:5173`)

## 📁 Project Structure

```
job_application_assistant/
├── backend/
│   ├── main.py                 # FastAPI application & API endpoints
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables (API keys)
│   ├── jobs_dataset.csv        # Job data
│   ├── training_data.csv       # Training data for ML models
│   ├── models/
│   │   ├── role_classifier.py  # ML role prediction model
│   │   └── train_models.py     # Model training script
│   └── services/
│       ├── ai_service.py       # Core AI service (Groq/OpenAI)
│       ├── resume_parser.py    # Resume text & skill extraction
│       ├── ats_engine.py       # ATS score calculation
│       ├── job_matcher.py      # Job matching algorithm
│       ├── skill_gap.py        # Skill gap analysis
│       ├── career_advisor.py   # Career feedback generation
│       ├── cover_letter_generator.py  # AI cover letter creation
│       ├── interview_prep.py   # Interview questions & tips
│       ├── salary_negotiator.py # Salary insights & strategies
│       └── job_search.py       # Job search functionality
│
└── ai-frontend/
    ├── src/
    │   ├── App.jsx             # Main application component
    │   ├── App.css             # Global styles
    │   ├── components/
    │   │   ├── Sidebar.jsx     # Navigation sidebar
    │   │   ├── Chat.jsx        # AI chat interface
    │   │   ├── ResumeAnalysis.jsx    # Resume upload & analysis
    │   │   ├── CoverLetter.jsx        # Cover letter generator
    │   │   ├── InterviewPrep.jsx      # Interview preparation
    │   │   ├── SalaryNegotiation.jsx  # Salary insights
    │   │   ├── JobSearch.jsx          # Job search
    │   │   └── ResultDisplay.jsx      # Results display
    │   └── api/
    │       └── backend.js      # API client
    ├── package.json
    └── vite.config.js
```

## 🔧 API Endpoints

### Resume Analysis
- `POST /analyze` - Analyze resume against job description

### Cover Letters
- `POST /cover-letter` - Generate detailed cover letter
- `POST /cover-letter/quick` - Quick cover letter generation

### Interview Prep
- `POST /interview-prep` - Get interview questions and tips
- `POST /interview-prep/answer-help` - Get help with specific questions

### Salary Insights
- `POST /salary-insights` - Get salary market data
- `POST /salary-insights/negotiation-email` - Generate negotiation email

### Job Search
- `POST /jobs/search` - Search for jobs
- `POST /jobs/match` - Match jobs to skills
- `POST /internships/search` - Search for internships

### Misc
- `GET /` - API documentation
- `GET /health` - Health check

## 🎨 Technologies Used

### Backend
- **FastAPI** - Modern Python web framework
- **Pandas** - Data manipulation
- **Scikit-learn** - Machine learning models
- **spaCy** - NLP for text processing
- **PDFPlumber** - PDF text extraction
- **Groq/OpenAI** - Advanced AI completion

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **Axios** - HTTP client
- **CSS3** - Styling with gradients & animations

## 🔐 API Keys & Configuration

### Getting Groq API Key (Recommended)
1. Visit [Groq Console](https://console.groq.com)
2. Sign up for a free account
3. Generate an API key
4. Add to `backend/.env`: `GROQ_API_KEY=your_key_here`

### Alternative: OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com)
2. Create an account and add payment method
3. Generate an API key
4. Add to `backend/.env`: `OPENAI_API_KEY=your_key_here`

**Note**: Groq is recommended as it's free and fast. The application provides fallback responses if no API key is configured.

## 🐛 Troubleshooting

### Backend Issues

**Port already in use**
```bash
# Change port in command
uvicorn main:app --reload --port 8001
```

**Module not found errors**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

**File not found: jobs_dataset.csv**
- Ensure the file exists in the backend directory
- Check the path in `main.py` and `services/job_matcher.py`

### Frontend Issues

**Port already in use**
- Vite will automatically try the next available port

**Cannot connect to backend**
- Ensure backend is running on port 8000
- Check the API URL in `src/api/backend.js`

**Blank page or errors**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run dev
```

## 📝 Usage Tips

1. **Resume Analysis**: Upload a PDF resume and paste the job description for best results
2. **Cover Letters**: Provide detailed information for more personalized letters
3. **Interview Prep**: Review questions and practice answers using the STAR method
4. **Salary Negotiation**: Research multiple sources and compare with our estimates
5. **Job Search**: Use specific keywords for better results

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- spaCy for NLP capabilities
- FastAPI for the amazing backend framework
- React team for the frontend library
- Groq for fast AI inference

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Made with ❤️ for job seekers worldwide**

🌟 Star this repo if you find it helpful!
