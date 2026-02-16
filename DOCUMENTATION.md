# AI Job Application Assistant - Documentation

## Table of Contents
- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Features](#features)
- [Installation](#installation)
- [API Reference](#api-reference)
- [Usage Guide](#usage-guide)
- [Technical Details](#technical-details)
- [Troubleshooting](#troubleshooting)

---

## Overview

The AI Job Application Assistant is a full-stack web application that helps job seekers optimize their resumes, discover job opportunities, and prepare for interviews. The platform combines algorithmic analysis with AI-powered insights to provide comprehensive career guidance.

### Key Capabilities
- **Resume Analysis**: ATS scoring with detailed feedback on format, keywords, and content
- **Skill Gap Analysis**: Identifies missing skills and generates personalized learning paths
- **Job Matching**: Matches candidates to relevant positions using multi-factor scoring
- **Live Job Search**: Real-time job listings from Adzuna API (2M+ jobs)
- **Interview Preparation**: Role-specific questions and answer frameworks
- **Cover Letter Generation**: Customized cover letters based on job descriptions
- **Salary Insights**: Market-based salary recommendations and negotiation strategies
- **AI Career Advisor**: Personalized career guidance and resume optimization tips

### Tech Stack
- **Backend**: Python 3.12, FastAPI
- **Frontend**: React 18, Vite
- **ML/NLP**: scikit-learn, spaCy
- **APIs**: Adzuna Jobs API, Groq LLM API
- **Data Processing**: pandas, numpy, pdfplumber

---

## System Architecture

### High-Level Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   React         │ ◄─────► │   FastAPI        │ ◄─────► │  External APIs  │
│   Frontend      │  HTTP   │   Backend        │  HTTP   │  (Adzuna, Groq) │
│   (Port 5174)   │         │   (Port 8000)    │         │                 │
└─────────────────┘         └──────────────────┘         └─────────────────┘
                                     │
                                     ▼
                            ┌──────────────────┐
                            │  Core Services   │
                            │  - ATS Engine    │
                            │  - Job Matcher   │
                            │  - Skill Analyzer│
                            │  - Resume Parser │
                            └──────────────────┘
```

### Backend Structure

```
backend/
├── main.py                      # FastAPI application & routes
├── services/
│   ├── ats_engine.py           # Resume scoring algorithms
│   ├── skill_gap.py            # Skill analysis & learning paths
│   ├── job_matcher.py          # Job matching algorithms
│   ├── job_search.py           # Adzuna API integration
│   ├── resume_parser.py        # PDF parsing & NLP extraction
│   ├── career_advisor.py       # AI career guidance
│   ├── interview_prep.py       # Interview question generation
│   ├── cover_letter_generator.py  # Cover letter creation
│   └── salary_negotiator.py    # Salary estimation
└── models/
    └── role_classifier.py      # ML-based role classification
```

### Frontend Structure

```
ai-frontend/
├── src/
│   ├── App.jsx                 # Main application
│   ├── components/
│   │   ├── ResumeAnalysis.jsx  # ATS scoring UI
│   │   ├── JobSearch.jsx       # Job search interface
│   │   ├── InterviewPrep.jsx   # Interview preparation
│   │   ├── CoverLetter.jsx     # Cover letter generator
│   │   ├── SalaryNegotiation.jsx  # Salary insights
│   │   └── Chat.jsx            # AI chat interface
│   └── api/
│       └── backend.js          # API client
```

---

## Features

### 1. Resume Analysis (ATS Scoring)

Upload a resume and job description to receive:
- **Overall ATS Score** (0-100)
- **Detailed Breakdown**:
  - Keyword match percentage
  - Content relevance score
  - Format quality score
- **Matched Keywords**: Skills found in your resume
- **Missing Keywords**: Important skills you should add
- **Actionable Recommendations**: Specific improvements

**Algorithm**: Combines TF-IDF vectorization (60%), keyword matching (25%), and format analysis (15%)

### 2. Skill Gap Analysis

Identifies skill gaps and generates learning paths:
- **Gap Analysis**: Shows which required skills are missing
- **Skill Categorization**: Critical vs. nice-to-have skills
- **Learning Path**: Step-by-step roadmap with prerequisites
- **Time Estimates**: Weeks needed to acquire each skill
- **Resource Recommendations**: Courses, documentation, practice projects

**Algorithm**: Uses fuzzy string matching (Jaccard similarity) and dependency graph resolution

### 3. Job Matching

Matches your profile to suitable positions:
- **Composite Match Score**: Weighted combination of 5 factors
  - Skill overlap (40%)
  - Title relevance (25%)
  - Experience level (20%)
  - Skill rarity bonus (10%)
  - Description similarity (5%)
- **Detailed Breakdown**: Score for each factor
- **Match Quality Indicator**: Excellent/Good/Fair/Poor

**Algorithm**: Multi-factor weighted scoring with TF-IDF weighting for rare skills

### 4. Live Job Search

Search real job listings:
- **2M+ Jobs**: Powered by Adzuna API
- **Filter Options**: Location, job type, experience level
- **Real Salaries**: Salary ranges in INR
- **Direct Applications**: One-click apply buttons
- **Internship Search**: Dedicated search for entry-level positions

### 5. Interview Preparation

Prepare with role-specific questions:
- **Technical Questions**: Based on your target role
- **Behavioral Questions**: STAR method scenarios
- **Smart Questions to Ask**: Shows your engagement
- **Answer Frameworks**: Structured approach to responses
- **Company Research Tips**: What to prepare

### 6. Cover Letter Generator

Create customized cover letters:
- **Resume-Based**: Uses your actual experience
- **Job-Specific**: Tailored to position requirements
- **Professional Tone**: Industry-appropriate language
- **Key Points**: Highlights relevant skills and achievements
- **Editable Output**: Copy and customize as needed

### 7. Salary Insights

Get market-informed salary guidance:
- **Salary Estimation**: Based on role, experience, location
- **Market Trends**: Demand and supply analysis
- **Negotiation Strategies**: Proven tactics and scripts
- **Skill Premium**: Value of your specific skills
- **Total Compensation**: Beyond base salary considerations

### 8. AI Career Advisor

Conversational career guidance:
- **Resume Feedback**: Comprehensive analysis
- **Career Path Advice**: Next steps and opportunities
- **Skill Development**: What to learn and why
- **File Upload Support**: Analyze specific documents
- **Context-Aware**: Remembers conversation history

---

## Installation

### Prerequisites
- Python 3.12+
- Node.js 18+
- npm or yarn

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd job_application_assistant
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

3. **Environment Variables**
   
   Create `backend/.env`:
   ```
   GROQ_API_KEY=your_groq_api_key
   ADZUNA_APP_ID=your_adzuna_app_id
   ADZUNA_API_KEY=your_adzuna_api_key
   ```

4. **Start Backend**
   ```bash
   uvicorn main:app --reload
   ```
   Backend runs on: http://localhost:8000

5. **Frontend Setup** (new terminal)
   ```bash
   cd ai-frontend
   npm install
   ```

6. **Start Frontend**
   ```bash
   npm run dev
   ```
   Frontend runs on: http://localhost:5174

### Getting API Keys

**Groq API** (Free tier available):
- Visit: https://console.groq.com
- Sign up and create API key
- Free: 30 requests/minute, 14,400/day

**Adzuna API** (Free tier available):
- Visit: https://developer.adzuna.com
- Register for developer account
- Get App ID and API Key
- Free: 250 calls/month

---

## API Reference

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Health Check
```http
GET /health
```
Response:
```json
{
  "status": "healthy",
  "timestamp": "2026-02-16T10:30:00"
}
```

#### 2. Resume Analysis (ATS)
```http
POST /ats/calculate
Content-Type: multipart/form-data

resume: <PDF file>
job_description: string
```

Response:
```json
{
  "overall_score": 72.5,
  "breakdown": {
    "keyword_match": 68.2,
    "format_quality": 100,
    "content_relevance": 75.4
  },
  "matched_keywords": ["python", "react", "aws"],
  "missing_keywords": ["kubernetes", "docker"],
  "recommendations": [...]
}
```

#### 3. Skill Gap Analysis
```http
POST /skill-gap/analyze
Content-Type: application/json

{
  "current_skills": ["python", "sql"],
  "required_skills": ["python", "sql", "docker", "kubernetes"]
}
```

Response:
```json
{
  "gap_percentage": 50.0,
  "missing_skills": {
    "critical": ["docker", "kubernetes"],
    "nice_to_have": []
  },
  "learning_path": [...],
  "time_estimate": "8 weeks"
}
```

#### 4. Job Matching
```http
POST /job-matcher/match
Content-Type: multipart/form-data

resume: <PDF file>
target_role: "Software Engineer"
```

Response:
```json
{
  "match_score": 78.5,
  "breakdown": {
    "skill_overlap": 85.0,
    "title_relevance": 90.0,
    "experience_match": 70.0,
    "skill_rarity_bonus": 15.0,
    "description_similarity": 65.0
  },
  "quality": "Good Match"
}
```

#### 5. Job Search
```http
POST /jobs/search
Content-Type: application/json

{
  "keywords": "Python Developer",
  "location": "Bangalore",
  "max_results": 20
}
```

Response:
```json
{
  "jobs": [
    {
      "title": "Senior Python Developer",
      "company": "Tech Corp",
      "location": "Bangalore",
      "salary": "₹15,00,000 - ₹20,00,000",
      "description": "...",
      "url": "https://..."
    }
  ],
  "count": 20
}
```

#### 6. Interview Preparation
```http
POST /interview/prepare
Content-Type: application/json

{
  "role": "Data Scientist",
  "experience_level": "mid"
}
```

Response:
```json
{
  "technical_questions": [...],
  "behavioral_questions": [...],
  "questions_to_ask": [...],
  "preparation_tips": [...]
}
```

#### 7. Cover Letter Generation
```http
POST /cover-letter/generate
Content-Type: multipart/form-data

resume: <PDF file>
job_description: string
company_name: string
job_title: string
```

Response:
```json
{
  "cover_letter": "Dear Hiring Manager, ...",
  "key_points": [...]
}
```

#### 8. Salary Insights
```http
POST /salary/negotiate
Content-Type: application/json

{
  "job_title": "Software Engineer",
  "experience_years": 5,
  "location": "Bangalore",
  "skills": ["python", "react", "aws"]
}
```

Response:
```json
{
  "salary_range": "₹15L - ₹25L per year",
  "market_analysis": "...",
  "negotiation_strategy": "...",
  "key_factors": [...]
}
```

#### 9. Career Advisor Chat
```http
POST /chat
Content-Type: application/json

{
  "message": "How can I improve my resume?",
  "context": {...}
}
```

Response:
```json
{
  "response": "Here are some suggestions...",
  "suggestions": [...]
}
```

---

## Usage Guide

### Uploading a Resume

1. Click "Choose File" button
2. Select PDF resume (max 10MB)
3. Wait for upload confirmation
4. Resume details extracted automatically

### Analyzing ATS Score

1. Upload your resume
2. Paste the job description
3. Click "Calculate ATS Score"
4. Review breakdown and recommendations
5. Update resume based on suggestions
6. Re-analyze to track improvement

### Searching for Jobs

1. Enter job title or keywords
2. Specify location (city or country)
3. Select job type (if needed)
4. Click "Search Jobs"
5. Browse results with salary info
6. Click "Apply Now" for direct links

### Preparing for Interviews

1. Enter target job role
2. Specify experience level
3. Generate questions
4. Review technical and behavioral questions
5. Practice answers using STAR method
6. Prepare questions to ask interviewers

### Getting Career Advice

1. Navigate to Career Advisor
2. Upload resume (optional)
3. Ask specific questions
4. Receive personalized guidance
5. Follow actionable recommendations

---

## Technical Details

### Core Algorithms

#### TF-IDF Vectorization
Used for resume-job description similarity:
- Converts text to numerical vectors
- Accounts for word importance (rare words weighted higher)
- Calculates cosine similarity between documents
- Complexity: O(n*m) where n=resume length, m=job description length

#### Fuzzy String Matching
Used for skill name variations:
- Jaccard similarity: intersection/union of character sets
- Handles variations: "reactjs" ↔ "react", "nodejs" ↔ "node.js"
- Threshold: 0.6 similarity considered a match
- Complexity: O(k) where k=average skill name length

#### Multi-Factor Composite Scoring
Used for job matching:
- 5 different scoring factors combined
- Weights: skills (40%), title (25%), experience (20%), rarity (10%), description (5%)
- Normalizes each factor to 0-100 scale
- Final score = weighted sum

#### Dependency Graph Resolution
Used for learning paths:
- Builds directed graph of skill prerequisites
- Topological sort for optimal learning order
- Example: Learn JavaScript → React → Redux
- Complexity: O(n + e) where n=skills, e=dependencies

### External Libraries

- **scikit-learn**: TF-IDF vectorization, cosine similarity
- **spaCy**: Named entity recognition, text processing
- **pdfplumber**: PDF text extraction
- **pandas**: Data manipulation for job datasets
- **FastAPI**: Async web framework with automatic API docs

### API Integrations

#### Adzuna Jobs API
- Aggregates 2M+ job listings worldwide
- Real-time data from multiple job boards
- Supports location, keyword, and salary filters
- Rate limit: 250 calls/month (free tier)

#### Groq API
- Fast LLM inference (llama-3.1-8b-instant)
- Used for text generation tasks only
- Average response time: 1-2 seconds
- Rate limit: 30 requests/minute (free tier)

---

## Troubleshooting

### Backend Issues

**Issue**: `ModuleNotFoundError: No module named 'fastapi'`
- **Solution**: Activate virtual environment and reinstall dependencies
  ```bash
  venv\Scripts\activate
  pip install -r requirements.txt
  ```

**Issue**: `spacy.cli.download() Connection Error`
- **Solution**: Manual download
  ```bash
  python -m spacy download en_core_web_sm
  ```

**Issue**: `RuntimeError: Could not load model en_core_web_sm`
- **Solution**: Ensure spaCy model is installed
  ```bash
  python -c "import spacy; spacy.load('en_core_web_sm')"
  ```

**Issue**: Port 8000 already in use
- **Solution**: Kill existing process or use different port
  ```bash
  uvicorn main:app --reload --port 8001
  ```

### Frontend Issues

**Issue**: `npm install` fails
- **Solution**: Clear cache and retry
  ```bash
  npm cache clean --force
  npm install
  ```

**Issue**: CORS errors in browser console
- **Solution**: Verify backend is running and CORS is configured
  - Check `backend/main.py` has CORS middleware
  - Ensure frontend URL matches allowed origins

**Issue**: API calls return 404
- **Solution**: Verify backend URL in `ai-frontend/src/api/backend.js`
  - Should be: `http://localhost:8000`

### API Key Issues

**Issue**: Groq API returns 401 Unauthorized
- **Solution**: Verify API key is correct in `.env`
  - Check for extra spaces or quotes
  - Regenerate key if necessary

**Issue**: Adzuna returns no results
- **Solution**: Check API quota and location format
  - Location should be: "City, Country" or just "Country"
  - Verify API credentials are active

### PDF Upload Issues

**Issue**: "File too large" error
- **Solution**: Ensure PDF is under 10MB
  - Compress PDF if necessary
  - Check file isn't corrupted

**Issue**: PDF parsing fails
- **Solution**: Verify PDF is text-based (not scanned image)
  - Try copying text from PDF manually
  - Convert image-based PDF to text using OCR

### Performance Issues

**Issue**: Slow API responses
- **Solution**: 
  - Check internet connection (external APIs)
  - Reduce number of job search results
  - Monitor Groq API rate limits
  - Clear browser cache

---

## Development

### Running Tests

Backend tests:
```bash
cd backend
python test_algorithms.py
```

### Adding New Features

1. **Backend**: Add new service in `backend/services/`
2. **Route**: Add endpoint in `backend/main.py`
3. **Frontend**: Create component in `ai-frontend/src/components/`
4. **API Client**: Add method in `ai-frontend/src/api/backend.js`

### Code Style

- **Python**: Follow PEP 8 guidelines
- **JavaScript**: Use ESLint configuration
- **Naming**: Use descriptive variable names
- **Documentation**: Add docstrings for all functions

---

## Deployment Considerations

### Backend Deployment

Recommended platforms:
- **Render**: Free tier available, easy setup
- **Railway**: Simple deployment, good free tier
- **Heroku**: Industry standard, paid tiers

Environment variables needed:
- `GROQ_API_KEY`
- `ADZUNA_APP_ID`
- `ADZUNA_API_KEY`
- `ENVIRONMENT=production`

### Frontend Deployment

Recommended platforms:
- **Vercel**: Optimized for React, free tier
- **Netlify**: Easy CI/CD, free tier
- **GitHub Pages**: Free but static only

Build command:
```bash
npm run build
```

### Production Checklist

- [ ] Environment variables set correctly
- [ ] CORS configured for production domain
- [ ] API rate limits considered
- [ ] Error logging configured
- [ ] HTTPS enabled
- [ ] .env files not committed
- [ ] Dependencies up to date
- [ ] Performance optimized

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

## Support

For questions or issues:
- Check this documentation first
- Review [ENGINEERING_DOCUMENTATION.md](ENGINEERING_DOCUMENTATION.md) for technical details
- Open an issue on GitHub for bugs or feature requests

---

**Built for job seekers worldwide** 🌍
