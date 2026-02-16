import os
import requests
from typing import List, Dict
from bs4 import BeautifulSoup
import re

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")
ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api/jobs"
INR_RATE = 83.0

def search_jobs(
    keywords: str,
    location: str = "",
    job_type: str = "",
    experience_level: str = ""
) -> List[Dict]:
    """Search for jobs based on criteria"""
    jobs = []

    if ADZUNA_APP_ID and ADZUNA_APP_KEY:
        jobs = _fetch_adzuna_jobs(
            keywords=keywords,
            location=location,
            job_type=job_type,
            experience_level=experience_level
        )
    
    if not jobs:
        jobs = generate_sample_jobs(keywords, location)
    
    # Filter by criteria
    if job_type:
        jobs = [j for j in jobs if j.get("type", "").lower() == job_type.lower()]
    
    if experience_level:
        jobs = [j for j in jobs if experience_level.lower() in j.get("experience_level", "").lower()]
    
    return jobs[:20]  # Return top 20


def search_internships(keywords: str, location: str = "") -> List[Dict]:
    """Search for internship opportunities"""
    internships = []

    if ADZUNA_APP_ID and ADZUNA_APP_KEY:
        internships = _fetch_adzuna_jobs(
            keywords=f"{keywords} internship",
            location=location,
            job_type="Internship",
            experience_level="Entry"
        )

    if not internships:
        internships = generate_sample_internships(keywords, location)
    return internships[:15]


def _fetch_adzuna_jobs(
    keywords: str,
    location: str,
    job_type: str,
    experience_level: str
) -> List[Dict]:
    """Fetch live jobs from Adzuna API"""
    country = "in"
    query_location = (location or "India").strip()

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": 20,
        "what": keywords,
        "where": query_location,
        "content-type": "application/json"
    }

    try:
        url = f"{ADZUNA_BASE_URL}/{country}/search/1"
        response = requests.get(url, params=params, timeout=20)
        if response.status_code != 200:
            return []

        data = response.json()
        results = data.get("results", [])

        jobs = []
        for item in results:
            salary_min = item.get("salary_min")
            salary_max = item.get("salary_max")
            currency = item.get("salary_currency") or "INR"

            salary_text = "Not disclosed"
            if salary_min or salary_max:
                if currency != "INR":
                    salary_min = int(salary_min * INR_RATE) if salary_min else None
                    salary_max = int(salary_max * INR_RATE) if salary_max else None
                    currency = "INR"
                if salary_min and salary_max:
                    salary_text = f"₹{salary_min:,.0f} - ₹{salary_max:,.0f}"
                elif salary_min:
                    salary_text = f"₹{salary_min:,.0f}+"
                elif salary_max:
                    salary_text = f"Up to ₹{salary_max:,.0f}"

            contract_type = (item.get("contract_type") or "").replace("_", " ").title()
            experience = "Entry-level" if "junior" in item.get("title", "").lower() else "Mid-level"

            jobs.append({
                "title": item.get("title"),
                "company": item.get("company", {}).get("display_name", ""),
                "location": item.get("location", {}).get("display_name", query_location),
                "type": contract_type or "Full-time",
                "experience_level": experience,
                "salary": salary_text,
                "description": (item.get("description") or "").strip()[:300] + "...",
                "skills_required": [],
                "posted": item.get("created") or "",
                "remote": "remote" in (item.get("title", "") + " " + item.get("description", "")).lower(),
                "apply_url": item.get("redirect_url")
            })

        if job_type:
            jobs = [j for j in jobs if job_type.lower() in (j.get("type", "").lower())]

        if experience_level:
            jobs = [j for j in jobs if experience_level.lower() in j.get("experience_level", "").lower()]

        return jobs
    except Exception:
        return []


def get_job_details(job_id: str) -> Dict:
    """Get detailed information about a specific job"""
    
    # In production, fetch from actual job boards
    return {
        "job_id": job_id,
        "title": "Software Engineer",
        "company": "Tech Corp",
        "location": "Remote",
        "salary_range": "$80,000 - $120,000",
        "description": "We're looking for a talented Software Engineer...",
        "requirements": [
            "3+ years of experience",
            "Proficiency in Python/JavaScript",
            "Strong problem-solving skills"
        ],
        "benefits": [
            "Health insurance",
            "401(k) matching",
            "Flexible work hours",
            "Remote work options"
        ],
        "posted_date": "2 days ago",
        "applicants": 45
    }


def generate_sample_jobs(keywords: str, location: str) -> List[Dict]:
    """Generate sample job listings"""
    
    keywords_lower = keywords.lower()
    
    job_templates = [
        {
            "title": "Senior Software Engineer",
            "company": "TechCorp",
            "location": location or "San Francisco, CA",
            "type": "Full-time",
            "experience_level": "Senior",
            "salary": "$120,000 - $160,000",
            "description": "Join our team building scalable cloud applications.",
            "skills_required": ["Python", "AWS", "Docker", "Kubernetes"],
            "posted": "2 days ago",
            "remote": True
        },
        {
            "title": "Data Scientist",
            "company": "DataInsights Inc",
            "location": location or "New York, NY",
            "type": "Full-time",
            "experience_level": "Mid-level",
            "salary": "$100,000 - $140,000",
            "description": "Build ML models to drive business insights.",
            "skills_required": ["Python", "Machine Learning", "SQL", "Statistics"],
            "posted": "1 week ago",
            "remote": True
        },
        {
            "title": "ML Engineer",
            "company": "AI Solutions",
            "location": location or "Austin, TX",
            "type": "Full-time",
            "experience_level": "Senior",
            "salary": "$130,000 - $170,000",
            "description": "Deploy and scale machine learning models in production.",
            "skills_required": ["Python", "TensorFlow", "MLOps", "AWS"],
            "posted": "3 days ago",
            "remote": True
        },
        {
            "title": "Frontend Developer",
            "company": "WebWorks",
            "location": location or "Remote",
            "type": "Full-time",
            "experience_level": "Mid-level",
            "salary": "$90,000 - $120,000",
            "description": "Create beautiful, responsive web applications.",
            "skills_required": ["React", "JavaScript", "CSS", "HTML"],
            "posted": "5 days ago",
            "remote": True
        },
        {
            "title": "Backend Developer",
            "company": "ServerSide Co",
            "location": location or "Seattle, WA",
            "type": "Full-time",
            "experience_level": "Mid-level",
            "salary": "$95,000 - $130,000",
            "description": "Build robust APIs and microservices.",
            "skills_required": ["Python", "FastAPI", "PostgreSQL", "Redis"],
            "posted": "1 day ago",
            "remote": False
        },
        {
            "title": "Full Stack Developer",
            "company": "StartupXYZ",
            "location": location or "Boston, MA",
            "type": "Full-time",
            "experience_level": "Mid-level",
            "salary": "$100,000 - $135,000",
            "description": "Work on both frontend and backend of our platform.",
            "skills_required": ["React", "Node.js", "MongoDB", "AWS"],
            "posted": "4 days ago",
            "remote": True
        },
        {
            "title": "DevOps Engineer",
            "company": "CloudOps",
            "location": location or "Remote",
            "type": "Full-time",
            "experience_level": "Senior",
            "salary": "$110,000 - $150,000",
            "description": "Manage our cloud infrastructure and CI/CD pipelines.",
            "skills_required": ["AWS", "Kubernetes", "Terraform", "Jenkins"],
            "posted": "1 week ago",
            "remote": True
        },
        {
            "title": "Junior Software Engineer",
            "company": "GrowthTech",
            "location": location or "Chicago, IL",
            "type": "Full-time",
            "experience_level": "Entry-level",
            "salary": "$70,000 - $90,000",
            "description": "Start your career with a supportive team.",
            "skills_required": ["Python", "Git", "SQL"],
            "posted": "2 days ago",
            "remote": False
        }
    ]
    
    # Filter jobs based on keywords
    filtered_jobs = []
    for job in job_templates:
        # Check if keywords match title, skills, or description
        if (keywords_lower in job["title"].lower() or
            keywords_lower in job["description"].lower() or
            any(keywords_lower in skill.lower() for skill in job["skills_required"])):
            filtered_jobs.append(job)
    
    # If no matches, return all jobs
    if not filtered_jobs:
        filtered_jobs = job_templates
    
    return filtered_jobs


def generate_sample_internships(keywords: str, location: str) -> List[Dict]:
    """Generate sample internship listings"""
    
    internship_templates = [
        {
            "title": "Software Engineering Intern",
            "company": "Google",
            "location": location or "Mountain View, CA",
            "duration": "12 weeks",
            "stipend": "$8,000/month",
            "description": "Work on real projects with mentorship from senior engineers.",
            "skills_required": ["Python", "Data Structures", "Algorithms"],
            "posted": "3 days ago",
            "application_deadline": "March 15, 2026"
        },
        {
            "title": "Data Science Intern",
            "company": "Microsoft",
            "location": location or "Redmond, WA",
            "duration": "10 weeks",
            "stipend": "$7,500/month",
            "description": "Build ML models for product recommendations.",
            "skills_required": ["Python", "Machine Learning", "Statistics"],
            "posted": "1 week ago",
            "application_deadline": "March 20, 2026"
        },
        {
            "title": "ML Engineering Intern",
            "company": "Meta",
            "location": location or "Menlo Park, CA",
            "duration": "12 weeks",
            "stipend": "$9,000/month",
            "description": "Deploy ML models at scale.",
            "skills_required": ["Python", "PyTorch", "Deep Learning"],
            "posted": "5 days ago",
            "application_deadline": "March 25, 2026"
        },
        {
            "title": "Frontend Development Intern",
            "company": "Airbnb",
            "location": location or "San Francisco, CA",
            "duration": "12 weeks",
            "stipend": "$7,000/month",
            "description": "Build user interfaces for millions of users.",
            "skills_required": ["React", "JavaScript", "CSS"],
            "posted": "4 days ago",
            "application_deadline": "March 18, 2026"
        },
        {
            "title": "Backend Engineering Intern",
            "company": "Amazon",
            "location": location or "Seattle, WA",
            "duration": "12 weeks",
            "stipend": "$8,500/month",
            "description": "Work on AWS services and infrastructure.",
            "skills_required": ["Java", "Python", "SQL"],
            "posted": "2 days ago",
            "application_deadline": "March 22, 2026"
        }
    ]
    
    return internship_templates


def match_jobs_to_skills(user_skills: List[str], jobs: List[Dict]) -> List[Dict]:
    """Match jobs to user skills and rank them"""
    
    scored_jobs = []
    
    for job in jobs:
        required_skills = job.get("skills_required", [])
        
        # Calculate match score
        matching_skills = set([s.lower() for s in user_skills]) & set([s.lower() for s in required_skills])
        match_score = (len(matching_skills) / len(required_skills)) * 100 if required_skills else 0
        
        job_with_score = job.copy()
        job_with_score["match_score"] = round(match_score, 1)
        job_with_score["matching_skills"] = list(matching_skills)
        job_with_score["missing_skills"] = [s for s in required_skills if s.lower() not in [us.lower() for us in user_skills]]
        
        scored_jobs.append(job_with_score)
    
    # Sort by match score
    scored_jobs.sort(key=lambda x: x["match_score"], reverse=True)
    
    return scored_jobs


def get_application_tips(job_title: str, company_name: str) -> Dict:
    """Get tips for applying to a specific job"""
    
    return {
        "resume_tips": [
            f"Highlight skills relevant to {job_title}",
            f"Research {company_name}'s values and culture",
            "Quantify your achievements with numbers",
            "Keep it concise and relevant (1-2 pages)"
        ],
        "cover_letter_tips": [
            f"Mention why you're interested in {company_name}",
            "Connect your experience to the job requirements",
            "Show enthusiasm and personality",
            "Keep it under 400 words"
        ],
        "application_checklist": [
            "Tailor your resume to the job description",
            "Write a compelling cover letter",
            "Update your LinkedIn profile",
            "Prepare your portfolio/GitHub",
            "Follow up after applying (wait 1-2 weeks)"
        ]
    }
