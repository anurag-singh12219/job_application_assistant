# API Reference - AI Job Application Assistant

Complete reference documentation for all REST API endpoints.

## Base URL

```
http://localhost:8000
```

## Interactive API Documentation

**Swagger UI**: http://localhost:8000/docs  
**ReDoc**: http://localhost:8000/redoc

---

## Endpoints Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/health` | Health check |
| `POST` | `/analyze` | Resume analysis & ATS scoring |
| `POST` | `/interview-prep` | Generate interview questions |
| `POST` | `/salary-insights` | Salary estimation & negotiation |
| `POST` | `/jobs/search` | Search live job listings |
| `POST` | `/jobs/match` | Match jobs to candidate profile |
| `POST` | `/cover-letter` | Generate cover letter |
| `POST` | `/chat` | AI career chat |
| `POST` | `/chat/upload` | Chat with file upload |

---

## Detailed Endpoint Documentation

### 1. Health Check

**Check if API is running and healthy**

```http
GET /health
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "service": "AI Job Application Assistant"
}
```

**Example (cURL):**
```bash
curl http://localhost:8000/health
```

---

### 2. Resume Analysis & ATS Scoring

**Analyze resume against job description using TF-IDF algorithm**

```http
POST /analyze
Content-Type: application/json
```

**Request Body:**
```json
{
  "resume_text": "John Doe\nSoftware Engineer\nPython, React, AWS, Docker\n5 years experience",
  "job_description": "Senior Python Developer with React and AWS knowledge required. Must have Docker experience."
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `resume_text` | string | Yes | Resume content (plain text or extracted from PDF) |
| `job_description` | string | Yes | Job description content |

**Response (200 OK):**
```json
{
  "overall_score": 78.5,
  "score_breakdown": {
    "tfidf_similarity": 82.0,
    "keyword_match_percentage": 75.5,
    "format_quality": 78.0
  },
  "matched_skills": [
    "Python",
    "React",
    "AWS",
    "Docker"
  ],
  "missing_skills": [],
  "critical_skills_matched": true,
  "action_verbs_found": ["developed", "implemented"],
  "recommendations": [
    "Excellent match - all required skills present",
    "Consider adding quantifiable achievements to resume",
    "Format is professional and well-structured"
  ]
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Resume text cannot be empty",
  "detail": "Please provide at least 10 characters of resume text"
}
```

**Example (cURL):**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Python developer with 5 years experience in FastAPI and React",
    "job_description": "Seeking Python developer with FastAPI expertise"
  }'
```

**Example (JavaScript/Axios):**
```javascript
import axios from 'axios';

const response = await axios.post('http://localhost:8000/analyze', {
  resume_text: "Your resume text here",
  job_description: "Your job description here"
});

console.log(response.data.overall_score);
```

---

### 3. Interview Preparation

**Generate role-specific interview questions with answer frameworks**

```http
POST /interview-prep
Content-Type: application/json
```

**Request Body:**
```json
{
  "job_title": "Senior Data Scientist",
  "job_description": "Looking for Data Scientist with ML, statistics, and SQL expertise",
  "skills": ["python", "tensorflow", "sql", "statistics"],
  "experience_years": 4
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `job_title` | string | Yes | Target job position |
| `job_description` | string | No | Job description for context |
| `skills` | array | No | List of candidate skills |
| `experience_years` | integer | No | Years of professional experience |

**Response (200 OK):**
```json
{
  "job_title": "Senior Data Scientist",
  "technical_questions": [
    {
      "question": "Walk us through your approach to building a predictive model for customer churn. What algorithms would you consider?",
      "category": "Technical",
      "difficulty": "Hard",
      "answer_framework": {
        "step_1": "Understand the problem - binary classification, imbalanced data",
        "step_2": "Data exploration - EDA, feature analysis",
        "step_3": "Feature engineering - create relevant features",
        "step_4": "Model selection - Logistic Regression, Random Forest, XGBoost",
        "step_5": "Evaluation - ROC-AUC, precision-recall for imbalanced data"
      }
    },
    {
      "question": "How do you handle missing data in categorical vs numerical features?",
      "category": "Technical",
      "difficulty": "Medium",
      "answer_framework": {
        "numerical": ["Mean/median imputation", "Forward/backward fill", "Model-based imputation"],
        "categorical": ["Mode imputation", "Create 'Unknown' category", "Predictive imputation"]
      }
    }
  ],
  "behavioral_questions": [
    {
      "question": "Tell us about a time you had to present complex technical findings to non-technical stakeholders.",
      "category": "Behavioral",
      "method": "STAR",
      "framework": {
        "S": "Situation",
        "T": "Task - Your responsibility",
        "A": "Action - What you did",
        "R": "Result - Positive outcome"
      }
    }
  ],
  "company_tips": [
    "Research the company's data stack and challenges",
    "Prepare examples using your technical skills",
    "Practice explaining ML concepts in simple terms",
    "Have questions ready about their data science team and challenges",
    "Discuss past projects and their impact"
  ],
  "estimated_prep_time_hours": 8
}
```

**Example (cURL):**
```bash
curl -X POST "http://localhost:8000/interview-prep" \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Machine Learning Engineer",
    "skills": ["python", "tensorflow", "sql"],
    "experience_years": 3
  }'
```

---

### 4. Salary Insights & Negotiation

**Get market-based salary estimation and negotiation guidance**

```http
POST /salary-insights
Content-Type: application/json
```

**Request Body:**
```json
{
  "job_title": "Senior Software Engineer",
  "location": "India",
  "experience_years": 5,
  "skills": ["python", "aws", "kubernetes", "machine-learning"]
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `job_title` | string | Yes | Job position |
| `location` | string | Yes | Geographic location (India, USA, etc.) |
| `experience_years` | integer | Yes | Years of professional experience |
| `skills` | array | No | List of technical skills (for premium calculation) |

**Response (200 OK):**
```json
{
  "job_title": "Senior Software Engineer",
  "location": "India",
  "experience_years": 5,
  "salary_estimate": {
    "base_salary": 1500000,
    "experience_bonus": 500000,
    "skill_premium": 250000,
    "total_estimated": 2250000,
    "currency": "INR",
    "usd_equivalent": 27000
  },
  "salary_range": {
    "low": 1800000,
    "average": 2250000,
    "high": 2800000
  },
  "percentile": {
    "rank": 65,
    "description": "Above average for this role and location"
  },
  "skill_premium_breakdown": {
    "python": 1.1,
    "aws": 1.15,
    "kubernetes": 1.2,
    "machine_learning": 1.25,
    "total_multiplier": 1.62
  },
  "negotiation_tips": [
    "Research market rates for your location and experience level",
    "Prepare specific examples of your impact and achievements",
    "Discuss total compensation including benefits, stock, bonus",
    "Be ready with your target salary range",
    "Practice negotiating professionally and confidently"
  ],
  "high_demand_skills": ["kubernetes", "machine_learning"],
  "negotiation_email_template": "As discussed, I am very interested in this Senior Software Engineer position. Based on my 5 years of experience, technical expertise in Python, AWS, and Kubernetes, and market research for similar roles in India, I believe a salary in the range of ₹20,00,000 - ₹25,00,000 annually is appropriate..."
}
```

**Example (cURL):**
```bash
curl -X POST "http://localhost:8000/salary-insights" \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Data Scientist",
    "location": "India",
    "experience_years": 3,
    "skills": ["python", "machine-learning", "sql"]
  }'
```

---

### 5. Live Job Search

**Search live job listings from Adzuna API (2M+ jobs)**

```http
POST /jobs/search
Content-Type: application/json
```

**Request Body:**
```json
{
  "keywords": "python developer",
  "location": "bangalore",
  "limit": 10
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `keywords` | string | Yes | Job search keywords (e.g., "python developer") |
| `location` | string | Yes | Location (city or country) |
| `limit` | integer | No | Number of results (default: 10, max: 50) |

**Response (200 OK):**
```json
{
  "count": 342,
  "jobs": [
    {
      "id": "job_12345",
      "title": "Senior Python Developer",
      "company": "TechCorp India",
      "location": "Bangalore, India",
      "salary_min": 1200000,
      "salary_max": 1800000,
      "currency": "INR",
      "description": "Looking for experienced Python developer with FastAPI and AWS knowledge...",
      "job_type": "permanent",
      "posted_date": "2024-02-10",
      "application_url": "https://jobs.example.com/apply/12345"
    },
    {
      "id": "job_12346",
      "title": "Python Backend Engineer",
      "company": "StartupXYZ",
      "location": "Bangalore, India",
      "salary_min": 900000,
      "salary_max": 1400000,
      "currency": "INR",
      "description": "Join our growing backend team. Work with Python, Django, and PostgreSQL...",
      "job_type": "permanent",
      "posted_date": "2024-02-09",
      "application_url": "https://jobs.example.com/apply/12346"
    }
  ]
}
```

**Error Response (unavailable Adzuna API):**
```json
{
  "message": "Live job data unavailable. Showing cached results.",
  "count": 5,
  "jobs": [
    {
      "title": "Sample Job - Configure Adzuna API for real data",
      "company": "Example Corp"
    }
  ]
}
```

**Example (JavaScript):**
```javascript
const response = await fetch('http://localhost:8000/jobs/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    keywords: 'machine learning engineer',
    location: 'bangalore',
    limit: 20
  })
});

const jobs = await response.json();
jobs.jobs.forEach(job => {
  console.log(`${job.title} at ${job.company}`);
});
```

---

### 6. Job Matching

**Match candidate skills to job listings with scoring**

```http
POST /jobs/match
Content-Type: application/json
```

**Request Body:**
```json
{
  "candidate_skills": ["python", "react", "aws", "docker"],
  "experience_years": 4,
  "target_salary_min": 1000000,
  "keywords": "full stack developer",
  "location": "bangalore",
  "limit": 10
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `candidate_skills` | array | Yes | List of candidate's skills |
| `experience_years` | integer | No | Years of professional experience |
| `target_salary_min` | integer | No | Minimum salary required |
| `keywords` | string | Yes | Job search keywords |
| `location` | string | Yes | Preferred location |
| `limit` | integer | No | Number of results (default: 10) |

**Response (200 OK):**
```json
{
  "candidate_profile": {
    "skills": ["python", "react", "aws", "docker"],
    "experience_years": 4,
    "target_salary_min": 1000000
  },
  "matches": [
    {
      "job_id": "job_12345",
      "title": "Senior Full Stack Developer",
      "company": "TechCorp",
      "location": "Bangalore",
      "salary_range": {
        "min": 1200000,
        "max": 1800000
      },
      "match_score": 87.5,
      "score_breakdown": {
        "skill_overlap": 90.0,
        "tfidf_similarity": 85.0,
        "critical_skills": 95.0,
        "experience_alignment": 80.0,
        "rarity_bonus": 80.0
      },
      "matched_skills": ["python", "react", "aws", "docker"],
      "missing_skills": ["kubernetes", "microservices"],
      "critical_skills_gap": "kubernetes (recommended)",
      "explanation": "Excellent match - you have all core skills required. Consider learning Kubernetes for better opportunities."
    },
    {
      "job_id": "job_12346",
      "title": "Backend Engineer - Python",
      "company": "StartupXYZ",
      "location": "Bangalore",
      "salary_range": {
        "min": 900000,
        "max": 1400000
      },
      "match_score": 76.2,
      "matched_skills": ["python", "docker"],
      "missing_skills": ["react", "aws"],
      "explanation": "Good match for backend role. Frontend skills not required for this position."
    }
  ],
  "recommendations": [
    "Top match is with TechCorp for Full Stack role",
    "Consider learning Kubernetes to improve match scores",
    "Your experience level aligns well with Senior positions",
    "Salary expectations match market rates for your profile"
  ]
}
```

**Example (cURL):**
```bash
curl -X POST "http://localhost:8000/jobs/match" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_skills": ["python", "machine-learning", "sql", "aws"],
    "experience_years": 3,
    "keywords": "data scientist",
    "location": "bangalore"
  }'
```

---

### 7. Cover Letter Generation

**Generate professional cover letters using AI**

```http
POST /cover-letter
Content-Type: application/json
```

**Request Body:**
```json
{
  "resume_text": "Senior Software Engineer with 5 years experience in Python, React, and AWS",
  "job_description": "Seeking Senior Python Developer to lead backend team. Requirements: Python, FastAPI, AWS, leader mindset",
  "job_title": "Senior Python Developer",
  "company_name": "TechCorp"
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `resume_text` | string | Yes | Your resume/professional background |
| `job_description` | string | Yes | Target job description |
| `job_title` | string | Yes | Target position title |
| `company_name` | string | No | Company name (for personalization) |

**Response (200 OK):**
```json
{
  "cover_letter": "Dear Hiring Manager,\n\nI am writing to express my strong interest in the Senior Python Developer position at TechCorp. With over 5 years of experience developing scalable Python applications using FastAPI and AWS, I am confident in my ability to lead your backend team and deliver high-quality solutions.\n\nThroughout my career, I have consistently demonstrated expertise in:\n\n- Building production-grade Python applications with FastAPI framework\n- Architecting and deploying solutions on AWS cloud infrastructure\n- Leading technical teams and mentoring junior developers\n- Designing and implementing efficient databases and APIs\n\nMy experience directly aligns with your requirements. I have successfully led backend teams, implemented fast and reliable APIs, and managed complex AWS infrastructure. I am particularly excited about TechCorp's mission and believe my technical expertise and leadership skills would make a significant contribution to your team.\n\nThank you for considering my application. I look forward to discussing how I can contribute to TechCorp's success.\n\nBest regards,\n[Your Name]",
  "style": "professional",
  "personalization": "company-specific"
}
```

**Example (cURL):**
```bash
curl -X POST "http://localhost:8000/cover-letter" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "John Doe - Data Scientist with Python and ML experience",
    "job_description": "Data Scientist needed with Python, TensorFlow, and SQL",
    "job_title": "Data Scientist",
    "company_name": "DataTech"
  }'
```

---

### 8. AI Career Chat

**Chat with AI about career questions**

```http
POST /chat
Content-Type: application/json
```

**Request Body:**
```json
{
  "message": "How do I transition from frontend to full-stack development?",
  "conversation_id": "conv_12345"
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | string | Yes | Your question or message |
| `conversation_id` | string | No | ID to maintain conversation context |

**Response (200 OK):**
```json
{
  "response": "Great question! Transitioning to full-stack development is a natural career progression. Here's a strategic approach:\n\n1. **Strengthen Backend Fundamentals**\n   - Learn a backend language (Python, Node.js, Java)\n   - Understand databases (SQL, NoSQL)\n   - Study API design and REST principles\n\n2. **Build Projects**\n   - Create full-stack projects from scratch\n   - Implement both frontend and backend\n   - Use version control (Git) throughout\n\n3. **Learn Deployment**\n   - Understand Docker containerization\n   - Learn cloud platforms (AWS, Azure, GCP)\n   - Set up CI/CD pipelines\n\n4. **Timeline**\n   - 3-6 months of focused learning\n   - Build 2-3 portfolio projects\n   - Start applying for junior full-stack roles\n\nWould you like specific recommendations for backend languages or project ideas?",
  "conversation_id": "conv_12345",
  "follow_up_suggestions": [
    "What backend language should I learn first?",
    "Can you recommend full-stack project ideas?",
    "What tools should I learn for deployment?"
  ]
}
```

**Example (JavaScript):**
```javascript
const chat = async (message) => {
  const response = await fetch('http://localhost:8000/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message: message,
      conversation_id: 'conv_123'
    })
  });
  
  const data = await response.json();
  console.log(data.response);
};

chat("How do I improve my system design skills?");
```

---

### 9. Chat with File Upload

**Upload resume and chat about it**

```http
POST /chat/upload
Content-Type: multipart/form-data
```

**Form Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | string | Yes | Your question about the file |
| `file` | file | Yes | PDF or text file (resume, cover letter, etc.) |
| `conversation_id` | string | No | Conversation context ID |

**Response (200 OK):**
```json
{
  "response": "I've reviewed your resume. Here are my observations:\n\n**Strengths:**\n- 5 years of solid Python development experience\n- Good technical skill set (React, AWS, Docker)\n- Clear career progression\n\n**Recommendations:**\n1. Add quantifiable achievements (% improvement, lines of code, etc.)\n2. Include specific project impacts and business results\n3. Highlight leadership or mentoring experiences\n4. Add certifications if relevant\n\nYour resume is strong overall. With these improvements, you'd be competitive for senior positions.",
  "extracted_info": {
    "file_type": "resume",
    "name": "John Doe",
    "experience_years": 5,
    "top_skills": ["Python", "React", "AWS"]
  }
}
```

**Example (JavaScript with FormData):**
```javascript
const uploadAndChat = async (file, message) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('message', message);
  
  const response = await fetch('http://localhost:8000/chat/upload', {
    method: 'POST',
    body: formData
  });
  
  const data = await response.json();
  console.log(data.response);
};

// Usage
const fileInput = document.querySelector('input[type="file"]');
uploadAndChat(fileInput.files[0], "Is my resume good for a senior role?");
```

---

## Error Handling

All endpoints return appropriate HTTP status codes and error messages.

### Common Error Responses

**400 Bad Request** - Invalid input
```json
{
  "error": "Resume text cannot be empty",
  "detail": "Please provide at least 10 characters of resume text"
}
```

**500 Internal Server Error** - Server processing error
```json
{
  "error": "Internal Server Error",
  "detail": "An unexpected error occurred while processing your request"
}
```

**503 Service Unavailable** - External API unavailable
```json
{
  "error": "Service temporarily unavailable",
  "detail": "The Adzuna Jobs API is currently unavailable. Returning cached results."
}
```

---

## Request/Response Format

All requests and responses use JSON format with UTF-8 encoding.

### Request Headers
```
Content-Type: application/json
Accept: application/json
```

### Response Headers
```
Content-Type: application/json; charset=utf-8
```

---

## Rate Limiting

Currently no rate limits are enforced in development. In production:
- API calls are limited to 100 requests per minute per IP
- File upload size limited to 10MB
- Job search limited to 50 results per request

---

## Testing with Postman

1. Download Postman from https://postman.com
2. Create new request
3. Select method (POST/GET)
4. Enter URL: `http://localhost:8000/analyze`
5. Go to "Body" tab
6. Select "raw" and "JSON"
7. Paste request JSON
8. Click "Send"

---

## Integration Examples

### Python
```python
import requests

response = requests.post(
    'http://localhost:8000/analyze',
    json={
        'resume_text': 'Your resume',
        'job_description': 'Job description'
    }
)
print(response.json())
```

### cURL
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"resume_text":"...","job_description":"..."}'
```

### JavaScript/Node.js
```javascript
fetch('http://localhost:8000/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    resume_text: '...',
    job_description: '...'
  })
})
.then(r => r.json())
.then(data => console.log(data))
```

---

## See Also

- [README.md](README.md) - Project overview
- [DOCUMENTATION.md](DOCUMENTATION.md) - Technical deep dive
- [SETUP.md](SETUP.md) - Installation and setup guide
- Interactive API Docs: http://localhost:8000/docs

---

**Last Updated**: February 2024  
**API Version**: 1.0
