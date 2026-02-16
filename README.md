# AI Job Application Assistant

A full-stack web application designed to help job seekers with resume optimization, job matching, interview preparation, and salary negotiation. The application combines classical algorithms with AI-powered features to provide actionable career guidance.

## Overview

This project implements both algorithmic and AI-driven approaches to address common challenges in the job search process:

- **Resume Analysis**: TF-IDF based scoring with comprehensive keyword extraction and format evaluation
- **Job Matching**: Multi-factor algorithm that weights skill relevance, experience alignment, and market opportunity
- **Interview Preparation**: Role-specific technical and behavioral question generation with answer frameworks
- **Salary Intelligence**: Market-based salary estimation and negotiation guidance
- **Career Chat**: Conversational AI interface for real-time career advice
- **Live Job Search**: Integration with live job market data

## Technology Stack

**Backend**: Python 3.12 | FastAPI | scikit-learn | spaCy | pandas | Groq API  
**Frontend**: React 18 | Vite | Axios | CSS3  
**Data**: Adzuna Jobs API | pdfplumber for PDF processing

---

## Features

### Resume Analysis & Scoring
Analyzes resumes against job descriptions using TF-IDF based scoring. The system extracts keywords, evaluates content relevance, and provides specific recommendations for improvement. Includes detection of action verbs, technical skills, and format quality assessment.

### Intelligent Job Matching
Matches candidate profiles to job listings by computing a composite score from multiple factors: skill overlap, experience alignment, and market demand. Access to live job market data through Adzuna API for real-time opportunities.

### Interview Preparation
Generates role-specific interview questions covering technical scenarios and behavioral topics using the STAR framework. Provides answer guidance and company-specific preparation strategies.

### Salary Insights & Negotiation
Provides market-based salary estimates and negotiation scripts. Includes location-based salary data and skill premium calculations to inform salary discussions.

### AI-Powered Chat
Conversational interface for career questions, resume reviews, and job guidance. Supports file uploads for in-context analysis and maintains conversation context for personalized advice.

### Cover Letter Generation
Creates customized cover letters based on resume content and job descriptions. Uses AI to ensure relevance and professional tone.

---

## Project Structure

```
job_application_assistant/
├── backend/
│   ├── main.py                          # FastAPI application
│   ├── requirements.txt                 # Python dependencies
│   ├── services/
│   │   ├── ats_engine.py               # Resume scoring algorithm
│   │   ├── skill_gap.py                # Skill analysis with fuzzy matching
│   │   ├── job_matcher.py              # Multi-factor job matching
│   │   ├── resume_parser.py            # PDF and text parsing
│   │   ├── career_advisor.py           # Career guidance generation
│   │   ├── salary_negotiator.py        # Salary estimation
│   │   ├── interview_prep.py           # Interview question generation
│   │   ├── cover_letter_generator.py   # Cover letter creation
│   │   ├── job_search.py               # Job search integration
│   │   └── llm_scaleup.py              # AI service wrapper
│   └── models/
│       └── role_classifier.py          # ML role prediction
│
├── ai-frontend/
│   ├── src/
│   │   ├── App.jsx                     # Main application component
│   │   ├── components/                 # React components
│   │   │   ├── Chat.jsx
│   │   │   ├── ResumeAnalysis.jsx
│   │   │   ├── UploadForm.jsx
│   │   │   └── ResultDisplay.jsx
│   │   ├── api/backend.js              # API client
│   │   └── styles/
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.10 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. Clone the repository and navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download the spaCy NLP model for resume parsing:
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env and add API keys (Groq, Adzuna - optional for basic functionality)
   ```

5. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
   The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd ai-frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   The application will open at `http://localhost:5173`

---

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/analyze` | POST | Analyze resume against job description |
| `/interview-prep` | POST | Generate interview questions |
| `/salary-insights` | POST | Get salary market data |
| `/job-search` | GET | Search for jobs by keywords and location |
| `/cover-letter` | POST | Generate cover letter |
| `/jobs/match` | POST | Match jobs to candidate profile |
| `/health` | GET | Health check |

Full API documentation available at `http://localhost:8000/docs`

---

## Technical Details

### Algorithms Used

- **TF-IDF Vectorization**: For document similarity and keyword weighting
- **Cosine Similarity**: Measuring resume-job description alignment
- **Fuzzy String Matching**: Handling skill name variations (e.g., "React" vs "ReactJS")
- **Graph-based Dependency Resolution**: For skill prerequisite mapping
- **Multi-factor Composite Scoring**: Weighted algorithm combining multiple scoring metrics
- **Linear Regression**: Salary estimation based on role, location, and experience

### Performance Considerations

The application is designed for rapid feedback with typical processing times:
- Resume analysis: < 1 second
- Job matching: < 2 seconds
- Interview question generation: < 5 seconds
- Salary estimation: < 500ms

API gracefully handles timeouts and relies on fallback data when external services are unavailable.

---

## Testing

To verify the installation works correctly:

```bash
# Run health check
curl http://localhost:8000/health

# Expected output:
# {"status":"healthy","service":"AI Job Application Assistant"}
```

---

## Troubleshooting

**Port already in use**: Change the port with `--port 8001` flag  
**Module import errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`  
**Cannot connect to backend**: Verify backend is running on port 8000 and check API URL in `src/api/backend.js`  
**Blank frontend page**: Clear browser cache and run `npm install && npm run dev` again  

---

## Contributing

Contributions are welcome. Please feel free to submit issues and pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues, please open an issue on GitHub or check the DOCUMENTATION.md file for more detailed technical information.

---

**Made for job seekers everywhere**
