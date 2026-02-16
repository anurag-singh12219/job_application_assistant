from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from typing import Dict, List

def calculate_ats(resume_text: str, job_desc: str) -> float:
    """Calculate ATS score with enhanced keyword matching and weighted analysis"""
    
    # Basic TF-IDF similarity (60% weight)
    tfidf = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))  # Include bigrams
    try:
        matrix = tfidf.fit_transform([resume_text, job_desc])
        tfidf_score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
    except:
        tfidf_score = 0.0
    
    # Keyword match score (25% weight)
    keyword_score = _calculate_keyword_match(resume_text, job_desc)
    
    # Format and structure score (15% weight)
    format_score = _evaluate_resume_format(resume_text)
    
    # Weighted final score
    final_score = (tfidf_score * 0.60) + (keyword_score * 0.25) + (format_score * 0.15)
    
    return round(final_score * 100, 2)


def calculate_detailed_ats(resume_text: str, job_desc: str) -> Dict:
    """Calculate detailed ATS analysis with breakdown and recommendations"""
    
    overall_score = calculate_ats(resume_text, job_desc)
    
    # Extract keywords from job description
    job_keywords = _extract_critical_keywords(job_desc)
    resume_keywords = _extract_critical_keywords(resume_text)
    
    # Find matches and gaps
    matched_keywords = [kw for kw in job_keywords if kw in resume_keywords]
    missing_keywords = [kw for kw in job_keywords if kw not in resume_keywords]
    
    # Analyze format quality
    format_analysis = {
        "has_contact_info": bool(re.search(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', resume_text)),  # Email
        "has_phone": bool(re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', resume_text)),  # Phone
        "has_sections": bool(re.search(r'(experience|education|skills|projects)', resume_text, re.IGNORECASE)),
        "has_quantifiable_achievements": bool(re.search(r'\d+%|\$\d+|\d+\+|increased|improved|reduced', resume_text, re.IGNORECASE)),
        "word_count": len(resume_text.split())
    }
    
    # Generate recommendations
    recommendations = _generate_ats_recommendations(
        overall_score,
        missing_keywords[:10],  # Top 10 missing keywords
        format_analysis
    )
    
    return {
        "overall_score": overall_score,
        "breakdown": {
            "keyword_match": round(len(matched_keywords) / max(len(job_keywords), 1) * 100, 1),
            "format_quality": round(format_analysis["has_sections"] * 100, 1),
            "content_relevance": round(_calculate_keyword_match(resume_text, job_desc) * 100, 1)
        },
        "matched_keywords": matched_keywords[:15],  # Show top 15 matches
        "missing_keywords": missing_keywords[:10],  # Show top 10 gaps
        "format_analysis": format_analysis,
        "recommendations": recommendations
    }


def _calculate_keyword_match(resume_text: str, job_desc: str) -> float:
    """Calculate keyword match score between resume and job description"""
    
    # Extract important keywords (skills, technologies, qualifications)
    job_keywords = set(_extract_critical_keywords(job_desc))
    resume_keywords = set(_extract_critical_keywords(resume_text))
    
    if not job_keywords:
        return 0.0
    
    # Calculate match percentage
    matched = job_keywords.intersection(resume_keywords)
    match_ratio = len(matched) / len(job_keywords)
    
    return match_ratio


def _extract_critical_keywords(text: str) -> List[str]:
    """Extract critical keywords (skills, technologies, qualifications) from text"""
    
    keywords = []
    text_lower = text.lower()
    
    # Common tech skills and tools
    tech_keywords = [
        'python', 'java', 'javascript', 'typescript', 'react', 'angular', 'vue',
        'node.js', 'express', 'django', 'flask', 'fastapi', 'spring', 'sql',
        'nosql', 'mongodb', 'postgresql', 'mysql', 'redis', 'aws', 'azure',
        'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'ci/cd', 'rest api',
        'graphql', 'microservices', 'machine learning', 'deep learning', 'nlp',
        'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'data science',
        'data analysis', 'statistics', 'a/b testing', 'tableau', 'power bi',
        'agile', 'scrum', 'jira', 'linux', 'bash', 'system design', 'selenium',
        'junit', 'pytest', 'html', 'css', 'sass', 'responsive design',
        'devops', 'mlops', 'langchain', 'llm', 'gpt', 'bert', 'transformers',
        'computer vision', 'opencv', 'data engineering', 'spark', 'hadoop',
        'airflow', 'kafka', 'elasticsearch', 'grafana', 'prometheus'
    ]
    
    # Find matching keywords
    for keyword in tech_keywords:
        if keyword in text_lower:
            keywords.append(keyword)
    
    # Extract degree keywords
    degree_keywords = ['bachelor', 'master', 'phd', 'mba', 'degree', 'diploma', 'certification']
    for keyword in degree_keywords:
        if keyword in text_lower:
            keywords.append(keyword)
    
    # Extract action verbs (important for ATS)
    action_verbs = [
        'developed', 'built', 'created', 'designed', 'implemented', 'deployed',
        'managed', 'led', 'optimized', 'improved', 'increased', 'reduced',
        'architected', 'engineered', 'automated', 'scaled', 'mentored'
    ]
    for verb in action_verbs:
        if verb in text_lower:
            keywords.append(verb)
    
    return list(set(keywords))  # Remove duplicates


def _evaluate_resume_format(resume_text: str) -> float:
    """Evaluate resume formatting and structure quality"""
    
    score = 0.0
    checks = 0
    
    # Check for contact information
    has_email = bool(re.search(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', resume_text))
    has_phone = bool(re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', resume_text))
    checks += 2
    score += (1 if has_email else 0) + (1 if has_phone else 0)
    
    # Check for standard sections
    sections = ['experience', 'education', 'skills', 'projects', 'summary']
    section_count = sum(1 for section in sections if section in resume_text.lower())
    checks += 1
    score += 1 if section_count >= 3 else (section_count / 3)
    
    # Check for quantifiable achievements
    has_metrics = bool(re.search(r'\d+%|\$\d+|\d+\+|increased|improved|reduced', resume_text, re.IGNORECASE))
    checks += 1
    score += 1 if has_metrics else 0
    
    # Check for action verbs
    action_verbs = ['developed', 'built', 'created', 'designed', 'implemented', 'led', 'managed']
    has_action_verbs = any(verb in resume_text.lower() for verb in action_verbs)
    checks += 1
    score += 1 if has_action_verbs else 0
    
    # Check word count (400-800 words is ideal)
    word_count = len(resume_text.split())
    checks += 1
    if 400 <= word_count <= 800:
        score += 1
    elif 300 <= word_count <= 1000:
        score += 0.7
    else:
        score += 0.4
    
    return score / checks if checks > 0 else 0.0


def _generate_ats_recommendations(score: float, missing_keywords: List[str], format_analysis: Dict) -> List[str]:
    """Generate specific recommendations to improve ATS score"""
    
    recommendations = []
    
    # Score-based recommendations
    if score < 60:
        recommendations.append("🚨 Critical: Your resume needs significant optimization to pass ATS screening")
        recommendations.append("Add more relevant keywords from the job description throughout your resume")
    elif score < 75:
        recommendations.append("⚠️ Your resume may struggle with strict ATS systems - improvements recommended")
    else:
        recommendations.append("✅ Good ATS compatibility - minor tweaks can push you to the top")
    
    # Keyword recommendations
    if missing_keywords:
        top_missing = ', '.join(missing_keywords[:5])
        recommendations.append(f"📝 Add these high-priority keywords: {top_missing}")
        recommendations.append("Naturally incorporate missing keywords in your experience and skills sections")
    
    # Format recommendations
    if not format_analysis.get("has_contact_info"):
        recommendations.append("📧 Add clear contact information (email, phone, LinkedIn)")
    
    if not format_analysis.get("has_sections"):
        recommendations.append("📑 Use standard section headers: Experience, Education, Skills, Projects")
    
    if not format_analysis.get("has_quantifiable_achievements"):
        recommendations.append("📊 Add quantifiable achievements (e.g., 'Increased performance by 40%', 'Led team of 5')")
    
    word_count = format_analysis.get("word_count", 0)
    if word_count < 300:
        recommendations.append("📝 Expand your resume - add more detail about your accomplishments and projects")
    elif word_count > 1000:
        recommendations.append("✂️ Shorten your resume - focus on most relevant and recent experiences")
    
    # General best practices
    recommendations.append("💡 Use action verbs: 'developed', 'implemented', 'led', 'optimized'")
    recommendations.append("🎯 Tailor your resume for each application - match job description language")
    
    return recommendations
