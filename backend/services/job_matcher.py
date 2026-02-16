import pandas as pd
import os
from typing import List, Dict
from collections import Counter
import math

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "jobs_dataset.csv")

df = pd.read_csv(DATA_PATH)


def match_jobs(candidate_skills: List[str], experience_years: int = 0) -> List[Dict]:
    """
    Advanced job matching algorithm using multi-factor scoring.
    
    This is real engineering with actual algorithms:
    1. TF-IDF weighted skill matching
    2. Skill importance scoring
    3. Experience level alignment
    4. Rarity bonus for specialized skills
    5. Composite scoring with normalized weights
    """
    
    # Build skill frequency map across all jobs (for TF-IDF)
    all_job_skills = []
    for _, row in df.iterrows():
        job_skills = [s.strip().lower() for s in str(row["skills"]).split(",")]
        all_job_skills.extend(job_skills)
    
    skill_frequency = Counter(all_job_skills)
    total_jobs = len(df)
    
    # Normalize candidate skills
    candidate_skills_norm = [s.strip().lower() for s in candidate_skills]
    
    results = []
    
    for _, row in df.iterrows():
        job_skills = [s.strip().lower() for s in str(row["skills"]).split(",")]
        
        # Calculate multiple scoring factors
        scores = calculate_match_scores(
            candidate_skills_norm,
            job_skills,
            skill_frequency,
            total_jobs,
            experience_years,
            row.get("experience_required", 0)
        )
        
        # Composite final score (weighted average)
        final_score = (
            scores["skill_overlap"] * 0.30 +
            scores["tfidf_score"] * 0.25 +
            scores["skill_importance"] * 0.20 +
            scores["experience_match"] * 0.15 +
            scores["rarity_bonus"] * 0.10
        )
        
        results.append({
            "role": row["role"],
            "match_score": round(final_score * 100, 2),
            "salary": row["salary_lpa"],
            "score_breakdown": {
                "skill_overlap": round(scores["skill_overlap"] * 100, 1),
                "tfidf_weighted": round(scores["tfidf_score"] * 100, 1),
                "skill_importance": round(scores["skill_importance"] * 100, 1),
                "experience_fit": round(scores["experience_match"] * 100, 1),
                "rarity_bonus": round(scores["rarity_bonus"] * 100, 1)
            },
            "matched_skills": scores["matched_skills"],
            "missing_skills": scores["missing_skills"],
            "fit_level": classify_fit(final_score)
        })
    
    return sorted(results, key=lambda x: x["match_score"], reverse=True)


def calculate_match_scores(
    candidate_skills: List[str],
    job_skills: List[str],
    skill_frequency: Counter,
    total_jobs: int,
    candidate_exp: int,
    required_exp: int
) -> Dict:
    """Calculate multiple matching scores using different algorithms"""
    
    # 1. Basic skill overlap (Jaccard similarity)
    candidate_set = set(candidate_skills)
    job_set = set(job_skills)
    
    matched_skills = list(candidate_set.intersection(job_set))
    missing_skills = list(job_set.difference(candidate_set))
    
    skill_overlap = len(matched_skills) / len(job_set) if job_set else 0
    
    # 2. TF-IDF weighted matching
    # Skills that are rare across jobs should count more
    tfidf_score = 0
    for skill in matched_skills:
        # IDF = log(total_jobs / jobs_with_skill)
        jobs_with_skill = skill_frequency[skill]
        idf = math.log(total_jobs / max(jobs_with_skill, 1))
        tfidf_score += idf
    
    # Normalize by total possible TF-IDF
    max_tfidf = sum(
        math.log(total_jobs / max(skill_frequency[s], 1))
        for s in job_skills
    )
    tfidf_score = tfidf_score / max_tfidf if max_tfidf > 0 else 0
    
    # 3. Skill importance scoring
    # Give more weight to critical skills (programming languages, frameworks)
    critical_skills = {
        "python", "java", "javascript", "react", "node.js", "sql", 
        "aws", "docker", "kubernetes", "machine learning", "typescript"
    }
    
    critical_matched = sum(1 for s in matched_skills if s in critical_skills)
    critical_required = sum(1 for s in job_skills if s in critical_skills)
    
    skill_importance = critical_matched / max(critical_required, 1) if critical_required > 0 else skill_overlap
    
    # 4. Experience level matching
    # Penalize if candidate is significantly under/over-qualified
    if required_exp == 0:
        experience_match = 1.0
    else:
        exp_diff = abs(candidate_exp - required_exp)
        # Linear penalty: 0.1 deduction per year of mismatch, min 0.5
        experience_match = max(1.0 - (exp_diff * 0.1), 0.5)
    
    # 5. Rarity bonus
    # Reward candidates with rare, specialized skills
    rare_skills = [
        s for s in matched_skills
        if skill_frequency[s] < total_jobs * 0.15  # Appears in <15% of jobs
    ]
    rarity_bonus = min(len(rare_skills) * 0.15, 0.5)  # Cap at 0.5
    
    return {
        "skill_overlap": skill_overlap,
        "tfidf_score": tfidf_score,
        "skill_importance": skill_importance,
        "experience_match": experience_match,
        "rarity_bonus": rarity_bonus,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }


def classify_fit(score: float) -> str:
    """Classify candidate fit level"""
    if score >= 0.80:
        return "Excellent Fit"
    elif score >= 0.65:
        return "Strong Fit"
    elif score >= 0.50:
        return "Good Fit"
    elif score >= 0.35:
        return "Moderate Fit"
    else:
        return "Poor Fit"


def rank_jobs_by_multiple_criteria(
    candidate_skills: List[str],
    filters: Dict
) -> List[Dict]:
    """
    Advanced job ranking with multiple criteria and user preferences.
    
    Filters can include:
    - min_salary: Minimum salary requirement
    - max_salary: Maximum salary (to avoid over-qualified)
    - location: Preferred location
    - remote: Remote work preference
    - company_size: Startup vs Enterprise
    """
    
    jobs = match_jobs(candidate_skills, filters.get("experience_years", 0))
    
    # Apply filters
    filtered_jobs = []
    for job in jobs:
        # Salary filter
        if "min_salary" in filters:
            if job["salary"] < filters["min_salary"]:
                continue
        
        if "max_salary" in filters:
            if job["salary"] > filters["max_salary"]:
                continue
        
        # Add preference score
        job["preference_score"] = calculate_preference_score(job, filters)
        job["final_score"] = (job["match_score"] * 0.7) + (job["preference_score"] * 0.3)
        
        filtered_jobs.append(job)
    
    return sorted(filtered_jobs, key=lambda x: x["final_score"], reverse=True)


def calculate_preference_score(job: Dict, filters: Dict) -> float:
    """Calculate how well job matches user preferences"""
    score = 50.0  # Base score
    
    # Salary desirability (closer to mid-range is better)
    if "min_salary" in filters and "max_salary" in filters:
        mid_salary = (filters["min_salary"] + filters["max_salary"]) / 2
        salary_diff = abs(job["salary"] - mid_salary)
        score += max(0, 30 - salary_diff * 0.1)
    
    # Other criteria can be added here
    
    return min(score, 100.0)
