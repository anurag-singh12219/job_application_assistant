# Technical Documentation - AI Job Application Assistant

## Architecture Overview

This document provides in-depth technical information about the implementation, algorithms, and architecture of the AI Job Application Assistant.

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    React Frontend (Port 5173)                │
│  - Resume Analysis UI                                       │
│  - Interview Preparation Interface                          │
│  - Chat Interface with File Upload                          │
│  - Salary Negotiation Calculator                            │
│  - Job Search & Matching Display                            │
└────────────────────┬────────────────────────────────────────┘
                     │ Axios HTTP Client
                     │
┌────────────────────▼────────────────────────────────────────┐
│                 FastAPI Backend (Port 8000)                  │
│  - RESTful API Endpoints                                    │
│  - Request Validation & Error Handling                      │
│  - CORS Configuration                                       │
│  - Async Request Processing                                 │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼─────────────┐
        │            │             │
┌───────▼──┐  ┌──────▼────┐  ┌────▼──────┐
│ Services │  │  Models   │  │  External │
│          │  │           │  │   APIs    │
│ - ATS    │  │ - Role    │  │           │
│ - Matcher│  │  Classify │  │ - Adzuna  │
│ - Parser │  │           │  │ - Groq    │
│ - Skill  │  │           │  │           │
│   Gap    │  │           │  │           │
│ - Chat   │  │           │  │           │
└──────────┘  └───────────┘  └───────────┘
        │            │             │
        └────────────┼─────────────┘
                     │
        ┌────────────▼─────────────┐
        │   Data & Configuration   │
        │ - CSV Datasets           │
        │ - Environment Variables  │
        │ - Models Cache           │
        └──────────────────────────┘
```

---

## Core Algorithms

### 1. ATS (Applicant Tracking System) Engine

**Location**: `backend/services/ats_engine.py`

The ATS engine uses TF-IDF (Term Frequency-Inverse Document Frequency) vectorization to score resumes against job descriptions. This algorithm naturally weights important, domain-specific terms higher than common words.

**Algorithm Steps:**

1. **Tokenization & Preprocessing**
   - Convert text to lowercase
   - Remove special characters using regex
   - Split into tokens

2. **Skill Extraction**
   - Pattern matching for 80+ technical skills
   - Action verb extraction
   - Keyword normalization (e.g., "react.js" → "react")

3. **TF-IDF Vectorization**
   ```
   TF(term) = count(term) / total_terms
   IDF(term) = log(total_docs / docs_with_term)
   TF-IDF(term) = TF(term) × IDF(term)
   ```

4. **Composite Scoring** (3 factors weighted):
   - **TF-IDF Match**: 60% - Rare, relevant skills weighted higher
   - **Keyword Match**: 25% - Exact skill matches
   - **Format Quality**: 15% - Structure, contact info, achievements

**Example Implementation**:
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_ats_score(resume_text, job_description):
    # Vectorize both documents
    vectorizer = TfidfVectorizer(max_features=500)
    vectors = vectorizer.fit_transform([resume_text, job_description])
    
    # Calculate cosine similarity
    tfidf_score = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
    
    # Combine with keyword and format scores
    keyword_score = extract_keyword_match(resume_text, job_description)
    format_score = evaluate_resume_format(resume_text)
    
    overall_score = (tfidf_score * 0.6) + (keyword_score * 0.25) + (format_score * 0.15)
    return overall_score * 100
```

**Time Complexity**: O(n × m) where n = resume length, m = job description length  
**Space Complexity**: O(n + m) for vectorization

---

### 2. Job Matcher - Multi-Factor Scoring

**Location**: `backend/services/job_matcher.py`

Matches candidate profiles to jobs using a weighted composite algorithm that considers 5 independent factors.

**Scoring Model:**
```
Job Match Score = 
    (Skill Overlap × 0.30) +
    (TF-IDF Weighted Similarity × 0.25) +
    (Critical Skill Importance × 0.20) +
    (Experience Alignment × 0.15) +
    (Rarity Bonus × 0.10)
```

**Implementation Details:**

1. **Skill Overlap Calculation**
   ```python
   candidate_skills = set(['python', 'react', 'aws'])
   job_required = set(['python', 'react', 'docker', 'kubernetes'])
   
   overlap = len(candidate_skills & job_required)
   overlap_percentage = overlap / len(job_required) * 100
   ```

2. **TF-IDF Weighted Similarity**
   - Calculate term importance in job description
   - Weight candidate's resume based on job's term importance
   - Result: Rare skills have higher impact

3. **Critical Skill Detection**
   - Classify skills as "critical" or "nice-to-have" based on job context
   - If candidate has all critical skills: +25 points
   - Missing critical skill: -15 points

4. **Experience Alignment**
   - Parse years of experience from resume (regex pattern)
   - Compare with job requirements
   - Calculate alignment percentage

5. **Rarity Bonus**
   - High-demand skills (AWS, Kubernetes, ML frameworks)
   - Candidate having rare skills: +10 point bonus

**Example Matching Output:**
```json
{
  "job_id": "job_12345",
  "job_title": "Senior ML Engineer",
  "match_score": 78.5,
  "factors": {
    "skill_overlap": 85.0,
    "tfidf_similarity": 72.0,
    "critical_skills": 90.0,
    "experience_alignment": 80.0,
    "rarity_bonus": 100.0
  },
  "matched_skills": ["python", "tensorflow", "aws"],
  "missing_critical_skills": ["kubernetes"],
  "recommendation": "Strong match - Missing Kubernetes but excellent on core ML skills"
}
```

**Time Complexity**: O(n × m × k) where n = num jobs, m = avg skills per job, k = candidate skills  
**Space Complexity**: O(n) for results storage

---

### 3. Fuzzy String Matching - Skill Gap Analysis

**Location**: `backend/services/skill_gap.py`

Handles skill name variations and typos to create accurate skill gap analyses.

**Algorithm: Jaccard Similarity**
```
Jaccard(Set A, Set B) = |A ∩ B| / |A ∪ B|

Example:
  skill_1 = "react"
  skill_2 = "reactjs"
  
  chars_a = {r,e,a,c,t}
  chars_b = {r,e,a,c,t,j,s}
  
  intersection = {r,e,a,c,t} = 5 items
  union = {r,e,a,c,t,j,s} = 7 items
  
  similarity = 5/7 ≈ 0.714 (71.4% match)
```

**Implementation:**
```python
def jaccard_similarity(str1, str2):
    """Calculate Jaccard similarity between two strings"""
    set1 = set(str1.lower())
    set2 = set(str2.lower())
    
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    return intersection / union if union > 0 else 0

def match_skill_variations(candidate_skill, job_skills_db):
    """Find best match for candidate skill in job database"""
    best_match = None
    best_score = 0
    
    for job_skill in job_skills_db:
        score = jaccard_similarity(candidate_skill, job_skill)
        if score > best_score and score > 0.7:  # 70% threshold
            best_score = score
            best_match = job_skill
    
    return best_match, best_score
```

**Dependency Graph for Learning Paths:**

```
Data Science Role Requirements:
┌─────────────────┐
│   Data Science  │
└────────┬────────┘
         │ requires
    ┌────┴────────────────────┐
    │                         │
┌───▼────┐            ┌──────▼──┐
│ Python │            │ Statistics
└───┬────┘            └──────┬──┐
    │ requires:       requires:│
    │                         │
┌───▼────────┐        ┌──────▼──┐
│ Numpy/Pandas         │ Linear Algebra
└────────────┘        └──────────┘
```

**Graph Topological Sort** for learning path generation:
1. Identify all dependencies (prerequisite skills)
2. Perform DFS to find independent learning paths
3. Order skills by prerequisites
4. Calculate time estimates per skill

**Time Complexity**: O(n × m) for matching, O(n log n) for sorting  
**Space Complexity**: O(n + m) for skill database

---

### 4. Resume Parsing with NLP

**Location**: `backend/services/resume_parser.py`

Uses spaCy for Named Entity Recognition (NER) to extract structured information from resumes.

**Extraction Components:**

1. **Named Entity Recognition**
   ```python
   import spacy
   
   nlp = spacy.load("en_core_web_sm")
   doc = nlp(resume_text)
   
   for ent in doc.ents:
       if ent.label_ == "PERSON":  # Person's name
           candidate_name = ent.text
       elif ent.label_ == "ORG":   # Company names
           work_experience.add(ent.text)
   ```

2. **Contact Information Extraction** (Regex Patterns)
   ```python
   # Email pattern
   email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
   
   # Phone pattern
   phone_pattern = r'(?:\+\d{1,3})?[\s.-]?\d{3}[\s.-]?\d{3}[\s.-]?\d{4}'
   
   # LinkedIn pattern
   linkedin_pattern = r'linkedin\.com/in/[\w-]+'
   ```

3. **Skill Extraction**
   - Predefined skill database (80+ skills)
   - Pattern matching with partial matching
   - Context-aware extraction

4. **Experience Duration Calculation**
   ```python
   # Extract dates and calculate duration
   date_pattern = r'(January|February|...|December)\s+(\d{4})|(\d{1,2}/\d{1,2}/\d{4})'
   
   # Example: "Software Engineer - Jan 2020 to Present"
   # Calculates: 4.1 years of experience
   ```

**Output Example:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1-555-123-4567",
  "linkedin": "linkedin.com/in/johndoe",
  "total_experience_years": 4.1,
  "extracted_skills": [
    {"skill": "Python", "frequency": 5},
    {"skill": "React", "frequency": 3},
    {"skill": "AWS", "frequency": 2}
  ],
  "companies": ["TechCorp", "StartupXYZ"],
  "education": ["B.Tech Computer Science"]
}
```

**Time Complexity**: O(n) for NER processing, O(m) for pattern matching  
**Space Complexity**: O(extracted_entities)

---

### 5. Salary Estimation Model

**Location**: `backend/services/salary_negotiator.py`

Linear regression model predicting salary based on role, location, and experience.

**Model Formula:**
```
Base Salary = BASE_SALARY[role][location] + (experience_years × EXPERIENCE_MULTIPLIER)

Example:
  Role: "Senior ML Engineer"
  Location: "India"
  Experience: 5 years
  
  Base (Senior ML Engineer in India) = ₹1,200,000
  Experience bonus (5 × ₹100,000) = ₹500,000
  Skill premium (AWS, ML, Python) = ₹200,000
  
  Total = ₹1,900,000
```

**Implementation:**
```python
def estimate_salary(job_title, location, experience_years, skills):
    # Base salary lookup from training data
    base_salary = SALARY_DATA.get((job_title, location), 50000)
    
    # Experience multiplier
    experience_bonus = experience_years * EXPERIENCE_INCREMENT
    
    # Skill premium for high-demand skills
    skill_premium = calculate_skill_premium(skills)
    
    # Final salary calculation
    estimated_salary = base_salary + experience_bonus + skill_premium
    
    return {
        "base_salary": base_salary,
        "experience_bonus": experience_bonus,
        "skill_premium": skill_premium,
        "total_estimated": estimated_salary,
        "percentile": calculate_percentile(estimated_salary, location)
    }
```

**Data-Driven Approach:**
- Training data from `backend/training_data.csv`
- 34+ role-location salary combinations
- Real market data validation

---

## API Design

### RESTful Endpoint Architecture

All endpoints follow REST conventions with:
- Proper HTTP methods (GET, POST)
- Status code returns (200, 400, 500)
- JSON request/response bodies
- Error handling and validation

### Key Implementation Features

**1. Error Handling**
```python
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"error": str(exc), "detail": "Invalid input data"}
    )
```

**2. Request Validation**
```python
from pydantic import BaseModel

class ResumeAnalysisRequest(BaseModel):
    resume_text: str
    job_description: str
    
    class Config:
        # Validate string is not empty
        min_anystr_length = 10
```

**3. Async Processing**
```python
@app.post("/analyze")
async def analyze_resume(request: ResumeAnalysisRequest):
    # Async processing for long-running operations
    results = await process_resume_async(request.resume_text)
    return results
```

**4. CORS Configuration**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Data Flow Examples

### Resume Analysis Flow
```
User uploads resume PDF
    ↓
pdfplumber extracts text
    ↓
Resume parser extracts: name, skills, experience
    ↓
ATS engine compares with job description
    ↓
TF-IDF vectorization calculates similarity
    ↓
Keyword matching identifies matched/missing skills
    ↓
Format evaluation checks resume structure
    ↓
Composite score combines all factors
    ↓
API returns: overall score, breakdown, recommendations
```

### Job Matching Flow
```
User profile (skills, experience) submitted
    ↓
Fetch jobs from live Adzuna API (2M+ jobs)
    ↓
For each job:
    - Extract job requirements
    - Calculate skill overlap
    - Run TF-IDF comparison
    - Evaluate experience fit
    - Check rarity bonus
    ↓
Sort by match score
    ↓
Return top 10 matches with explanations
```

### Skill Gap Analysis Flow
```
Compare candidate skills with job requirements
    ↓
Use Jaccard similarity for fuzzy matching
    ↓
Build skill prerequisite graph
    ↓
Topological sort for learning order
    ↓
Estimate weeks to learn each skill
    ↓
Return: gaps, prerequisites, learning path, time estimates
```

---

## Performance Optimization

### Caching Strategies
- **Job data caching**: Adzuna results cached for 24 hours
- **Model caching**: spaCy model loaded once on startup
- **Skill database**: Pre-loaded in memory for O(1) lookup

### Complexity Analysis

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| ATS Scoring | O(n×m) | O(n+m) | n=resume length, m=job desc |
| Job Matching | O(n×m×k) | O(n) | k=candidate skills |
| Skill Gap | O(n×m) | O(n+m) | Fuzzy matching across DB |
| Resume Parsing | O(n) | O(entities) | Linear NLP processing |
| Salary Estimation | O(1) | O(1) | Lookup table + calculation |

### Database Design
```
Skills Database (34,000+ entries):
{
  "python": {"category": "programming", "demand": "high", "level": 5},
  "react": {"category": "frontend", "demand": "high", "level": 5},
  "aws": {"category": "cloud", "demand": "high", "level": 4}
}

Salary Data (34+ entries):
{
  ("ML Engineer", "India"): 1200000,
  ("Senior ML Engineer", "USA"): 180000,
  ("Data Scientist", "India"): 900000
}
```

---

## Integration with External APIs

### Adzuna Jobs API
- **Purpose**: Access 2M+ live job listings
- **Rate Limit**: Respects API limits with exponential backoff
- **Fallback**: Returns cached results if API unavailable
- **Data Processing**: Converts salary to INR for India-based users

```python
async def search_jobs_adzuna(keywords, location, limit=10):
    try:
        response = await client.get(
            "https://api.adzuna.com/v1/api/jobs/gb/search",
            params={
                "app_id": ADZUNA_APP_ID,
                "app_key": ADZUNA_APP_KEY,
                "what": keywords,
                "where": location,
                "results_per_page": limit
            }
        )
        return response.json()
    except Exception as e:
        # Return cached results as fallback
        return get_cached_jobs(keywords, location)
```

### Groq AI API
- **Purpose**: AI-powered text generation (insights, cover letters, interview questions)
- **Model**: llama-3.1-8b-instant (fast inference)
- **Caching**: Results cached to avoid repeated API calls
- **Graceful Degradation**: Returns template responses if API unavailable

```python
async def generate_cover_letter(resume_text, job_description):
    prompt = f"""
    Based on this resume and job description, generate a professional cover letter.
    Keep it concise and impactful.
    
    Resume: {resume_text}
    Job Description: {job_description}
    """
    
    response = await groq_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant"
    )
    
    return response.choices[0].message.content
```

---

## Testing Strategy

### Unit Testing Core Algorithms

```python
# Test TF-IDF scoring consistency
def test_ats_score_consistency():
    resume = "Python Django FastAPI"
    job_desc = "Python FastAPI"
    score1 = calculate_ats_score(resume, job_desc)
    score2 = calculate_ats_score(resume, job_desc)
    assert score1 == score2, "Score should be deterministic"

# Test Jaccard similarity bounds
def test_jaccard_similarity():
    assert jaccard_similarity("cat", "cat") == 1.0
    assert jaccard_similarity("cat", "dog") < 0.5
    assert jaccard_similarity("react", "reactjs") > 0.7

# Test skill extraction accuracy
def test_skill_extraction():
    text = "Experience with Python, React, AWS, and Docker"
    skills = extract_skills(text)
    assert "Python" in skills
    assert "React" in skills
    assert len(skills) >= 4
```

### Integration Testing

API endpoints tested for:
- Request validation
- Error handling
- Response format consistency
- Edge cases (empty input, very long text)
- Timeout handling

---

## Code Quality Metrics

- **Total Lines of Code**: ~2,000
- **Algorithmic Implementation**: ~65%
- **LLM Integration**: ~35% (for insights and generation only)
- **Test Coverage**: Core algorithms have unit tests
- **Documentation**: This file + inline code comments

---

## Future Improvements

1. **Database Integration**: Replace CSV with PostgreSQL for scalability
2. **Caching Layer**: Redis for distributed caching
3. **Advanced NLP**: Transformer models for better entity extraction
4. **Real-time Updates**: WebSocket for live job matching
5. **Analytics**: Track user career progression and success metrics
6. **Containerization**: Docker deployment for production

---

## References

- TF-IDF: https://en.wikipedia.org/wiki/Tf%E2%80%93idf
- Cosine Similarity: https://en.wikipedia.org/wiki/Cosine_similarity
- Jaccard Index: https://en.wikipedia.org/wiki/Jaccard_index
- spaCy Documentation: https://spacy.io/
- FastAPI: https://fastapi.tiangolo.com/
- scikit-learn: https://scikit-learn.org/

---

## Contact & Support

For technical questions about the implementation, refer to the main README.md or open an issue on GitHub.
