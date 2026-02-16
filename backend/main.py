from fastapi import FastAPI, UploadFile, Form, File, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import pandas as pd

from services.resume_parser import extract_text, extract_skills
from services.ats_engine import calculate_ats
from services.job_matcher import match_jobs
from services.skill_gap import find_gap
from services.career_advisor import generate_feedback
from services.cover_letter_generator import generate_cover_letter, generate_custom_cover_letter
from services.interview_prep import generate_interview_questions, generate_interview_tips, generate_answer_framework
from services.salary_negotiator import get_salary_insights, generate_negotiation_email, compare_offers
from services.job_search import search_jobs, search_internships, match_jobs_to_skills, get_application_tips
from models.role_classifier import predict_role

import os

app = FastAPI(
    title="AI Job Application Assistant",
    description="Complete AI-powered career assistance platform",
    version="2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic Models
class CoverLetterRequest(BaseModel):
    job_title: str
    company_name: str
    job_description: str
    user_name: Optional[str] = "Candidate"
    skills: List[str]
    tone: str = "professional"

class InterviewPrepRequest(BaseModel):
    job_title: str
    job_description: str
    company_name: Optional[str] = ""
    skills: List[str]

class SalaryRequest(BaseModel):
    job_title: str
    location: str
    experience_years: int
    skills: List[str]

class JobSearchRequest(BaseModel):
    keywords: str
    location: Optional[str] = ""
    job_type: Optional[str] = ""
    experience_level: Optional[str] = ""

class NegotiationEmailRequest(BaseModel):
    current_offer: int
    desired_salary: int
    justification: str


# Data
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "jobs_dataset.csv")

try:
    jobs_df = pd.read_csv(DATA_PATH)
except:
    jobs_df = pd.DataFrame()  # Empty dataframe if file not found


# =============== API ENDPOINTS ===============

@app.get("/")
async def root():
    return {
        "message": "AI Job Application Assistant API",
        "version": "2.0",
        "endpoints": {
            "resume_analysis": "/analyze",
            "cover_letter": "/cover-letter",
            "interview_prep": "/interview-prep",
            "salary_insights": "/salary-insights",
            "job_search": "/jobs/search",
            "internships": "/internships/search"
        }
    }


@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """Analyze resume against job description with comprehensive AI feedback"""
    try:
        # Extract text from resume
        text = extract_text(file.file)
        if not text or len(text) < 50:
            return {
                "error": "Unable to extract text from resume",
                "suggestion": "Please ensure your PDF is readable and contains text (not just images)"
            }
        
        # Extract skills
        skills = extract_skills(text)
        print(f"Extracted {len(skills)} skills: {skills}")

        if not skills:
            return {
                "error": "No technical skills found in resume",
                "suggestion": "Make sure your resume includes technical skills, programming languages, and tools you've used",
                "partial_analysis": {
                    "resume_length": len(text),
                    "has_content": True
                }
            }

        # Predict role and calculate ATS score
        predicted_role = predict_role(skills)
        ats = calculate_ats(text, job_description)
        print(f"Predicted role: {predicted_role}, ATS Score: {ats}")

        # Match jobs
        matches = match_jobs(skills)
        best = matches[0] if matches else {"role": predicted_role, "salary": 0, "match_score": 0}

        # Get required skills for role
        required = []
        if not jobs_df.empty and best["role"] in jobs_df["role"].values:
            role_data = jobs_df[jobs_df["role"] == best["role"]]
            if not role_data.empty and "skills" in role_data.columns:
                skills_str = role_data["skills"].values[0]
                if isinstance(skills_str, str):
                    required = [s.strip() for s in skills_str.split(",")]
        
        # Find skill gap
        gap = find_gap(skills, required)
        print(f"Skill gap: {gap}")
        
        # Generate AI-powered comprehensive feedback
        feedback = generate_feedback(
            skills=skills,
            role=best["role"],
            missing_skills=gap,
            ats_score=ats,
            resume_text=text,
            job_description=job_description
        )

        return {
            "skills": skills,
            "predicted_role": predicted_role,
            "recommended_role": best["role"],
            "ats_score": ats,
            "missing_skills": gap,
            "salary_estimate_lpa": best.get("salary", 0),
            "top_job_matches": matches[:5],
            "feedback": feedback,
            "resume_stats": {
                "total_words": len(text.split()),
                "total_skills": len(skills),
                "experience_level": "Entry" if len(skills) < 5 else "Mid" if len(skills) < 10 else "Senior"
            }
        }
    except Exception as e:
        print(f"Error in analyze_resume: {type(e).__name__}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/cover-letter")
async def create_cover_letter(request: CoverLetterRequest):
    """Generate AI-powered cover letter"""
    try:
        cover_letter = generate_cover_letter(
            job_title=request.job_title,
            company_name=request.company_name,
            job_description=request.job_description,
            resume_text="",  # Could be passed if needed
            skills=request.skills,
            tone=request.tone
        )
        
        return {
            "cover_letter": cover_letter,
            "tips": [
                "Personalize the greeting if possible",
                "Proofread carefully before sending",
                "Save as PDF to preserve formatting",
                "Mention specific company achievements or values"
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/cover-letter/quick")
async def quick_cover_letter(request: Dict = Body(...)):
    """Generate quick cover letter without full resume"""
    try:
        user_name = request.get("user_name", "Candidate")
        job_title = request.get("job_title", "")
        company_name = request.get("company_name", "")
        skills = request.get("skills", "")
        experience_years = request.get("experience_years", 0)
        
        # Handle skills as string or list
        if isinstance(skills, str):
            skills_list = [s.strip() for s in skills.split(",")]
        else:
            skills_list = skills
        
        cover_letter = generate_custom_cover_letter(
            user_name=user_name,
            job_title=job_title,
            company_name=company_name,
            skills=skills_list,
            experience_years=int(experience_years)
        )
        
        return {"cover_letter": cover_letter}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/interview-prep")
async def interview_preparation(request: InterviewPrepRequest):
    """Get interview preparation materials"""
    try:
        questions = generate_interview_questions(
            request.job_title,
            request.job_description,
            request.skills
        )
        
        tips = generate_interview_tips(request.job_title, request.company_name)
        
        return {
            "questions": questions,
            "preparation_tips": tips,
            "general_advice": [
                "Practice the STAR method for behavioral questions",
                "Research the company thoroughly",
                "Prepare 3-5 questions to ask the interviewer",
                "Review your resume and be ready to discuss each point",
                "Dress appropriately for the company culture"
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/interview-prep/answer-help")
async def get_answer_help(
    question: str = Body(...),
    job_context: str = Body(...)
):
    """Get help structuring an answer to a specific interview question"""
    try:
        framework = generate_answer_framework(question, job_context)
        return {"answer_framework": framework}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/salary-insights")
async def salary_negotiation(request: SalaryRequest):
    """Get salary insights and negotiation strategies"""
    try:
        insights = get_salary_insights(
            job_title=request.job_title,
            location=request.location,
            experience_years=request.experience_years,
            skills=request.skills
        )
        
        return insights
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/salary-insights/negotiation-email")
async def create_negotiation_email(request: NegotiationEmailRequest):
    """Generate salary negotiation email"""
    try:
        email = generate_negotiation_email(
            current_offer=request.current_offer,
            desired_salary=request.desired_salary,
            justification=request.justification
        )
        
        return {"email": email}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/jobs/search")
async def find_jobs(request: JobSearchRequest):
    """Search for job opportunities"""
    try:
        jobs = search_jobs(
            keywords=request.keywords,
            location=request.location,
            job_type=request.job_type,
            experience_level=request.experience_level
        )
        
        return {
            "total_results": len(jobs),
            "jobs": jobs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/jobs/match")
async def match_jobs_endpoint(skills: List[str] = Body(...)):
    """Match jobs to user skills"""
    try:
        jobs = search_jobs(keywords=" ".join(skills))
        matched_jobs = match_jobs_to_skills(skills, jobs)
        
        return {
            "matched_jobs": matched_jobs[:15],
            "your_skills": skills
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/internships/search")
async def find_internships(
    keywords: str = Body(...),
    location: str = Body("")
):
    """Search for internship opportunities"""
    try:
        internships = search_internships(keywords, location)
        
        return {
            "total_results": len(internships),
            "internships": internships
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/application-tips/{company_name}/{job_title}")
async def get_tips(company_name: str, job_title: str):
    """Get application tips for specific company and role"""
    try:
        tips = get_application_tips(job_title, company_name)
        return tips
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat")
async def career_chat(data: Dict = Body(...)):
    """AI Career Chat endpoint for general career advice"""
    try:
        query = data.get("query", "").strip()
        if not query:
            return {"advice": "Please ask a question about your career!"}
        
        # Use AI service to generate career advice
        from services.ai_service import ai_service
        
        prompt = f"""You are an expert career coach with 20+ years of experience. 
The user is asking about their career and job search journey. 

User Question: {query}

Provide practical, actionable, and encouraging advice. Be specific with examples where relevant.
Keep the response between 150-300 words. Use professional but friendly tone."""
        
        system_message = "You are a supportive and knowledgeable career coach. Provide practical advice that helps people succeed in their careers."
        
        advice = ai_service.generate_completion(
            prompt=prompt,
            max_tokens=400,
            temperature=0.7,
            system_message=system_message
        )
        
        return {
            "advice": advice,
            "response": advice
        }
    except Exception as e:
        print(f"Chat error: {e}")
        return {
            "advice": "I'm here to help with your career journey! Try asking me about resumes, interviews, salary negotiation, or job search strategies.",
            "response": "I'm here to help with your career journey! Try asking me about resumes, interviews, salary negotiation, or job search strategies."
        }


@app.post("/chat/with-file")
async def career_chat_with_file(
    file: UploadFile = File(...),
    query: str = Form("")
):
    """AI Career Chat endpoint that uses uploaded file content"""
    try:
        from services.ai_service import ai_service

        text = extract_text(file.file)
        if not text:
            raise HTTPException(status_code=400, detail="Unable to read text from the uploaded file")

        skills = extract_skills(text)
        excerpt = text[:1500]
        question = query.strip() or "Please analyze the uploaded file and provide career advice based on its content."

        prompt = f"""You are an expert career coach. The user uploaded a file and asked a question.

User Question:
{question}

Extracted Skills (if any): {', '.join(skills[:20])}

File Excerpt:
{excerpt}

Provide a helpful, realistic response grounded in the file content. Avoid placeholders.
"""

        advice = ai_service.generate_completion(
            prompt=prompt,
            max_tokens=500,
            temperature=0.6,
            system_message="You are a practical, supportive career coach. Use the uploaded file context in your response."
        )

        return {
            "advice": advice,
            "response": advice,
            "extracted_skills": skills[:25]
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Chat file error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process uploaded file")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "AI Job Application Assistant"}
