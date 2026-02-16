from .ai_service import ai_service
from typing import Dict
import statistics

def get_salary_insights(
    job_title: str,
    location: str,
    experience_years: int,
    skills: list
) -> Dict:
    """Get AI-powered salary insights and negotiation strategies with real market data"""
    
    # Estimate salary based on role, experience, and location
    salary_estimate = estimate_salary(job_title, experience_years, location)
    
    currency_symbol = "₹" if salary_estimate["currency"] == "INR" else "$"
    location_text = f"in {location}"
    
    # Enhanced AI prompt for more accurate, market-based advice
    prompt = f"""You are a professional salary negotiation consultant with 15+ years of experience. Provide highly specific, data-driven salary negotiation insights:

**Candidate Profile:**
- Job Title: {job_title}
- Location: {location}
- Experience: {experience_years} years
- Key Skills: {', '.join(skills[:8])}

**Current Market Data (2024):**
- Estimated Salary Range: {currency_symbol}{salary_estimate['min']:,} - {currency_symbol}{salary_estimate['max']:,} {salary_estimate['currency']}
- Market demand for {job_title} in {location} is {"high" if experience_years >= 3 else "moderate"}

**Provide detailed analysis:**

1. **Market Analysis** (100 words):
   - Current hiring trends for {job_title} in {location}
   - Industry-specific factors affecting compensation
   - How candidate's experience level ({experience_years} years) compares to market average
   - Supply/demand dynamics for this role

2. **Salary Enhancement Factors** (5-7 specific points):
   - Which of these skills ({', '.join(skills[:5])}) command premium compensation
   - Certifications or achievements that could increase offers by 10-20%
   - Company types (startups vs. established) that pay more
   - Remote work considerations

3. **Proven Negotiation Strategies** (4-5 tactics with exact scripts):
   - Specific phrases to use when discussing compensation
   - How to counter lowball offers professionally
   - Timing strategy: when to negotiate (before/after offer)
   - How to leverage competing offers
   - Non-salary benefits to negotiate (equity, signing bonus, remote work)

4. **Red Flags & Warning Signs** (3-4 points):
   - Salary offers that seem unusually low or high
   - Pressure tactics to accept quickly
   - Vague compensation structures

5. **Professional Communication Script**:
   - Exact email template for salary negotiation
   - Phone conversation talking points

Provide real, actionable advice based on actual market conditions. Be specific with numbers, percentages, and concrete examples. Total: 400-500 words."""
    
    ai_advice = ai_service.generate_completion(prompt, max_tokens=1500, temperature=0.7)
    
    # Generate detailed breakdown with AI insights
    industry_insights = _get_industry_insights(job_title, location, experience_years, currency_symbol)
    
    return {
        "estimated_salary_range": salary_estimate,
        "negotiation_advice": ai_advice,
        "industry_insights": industry_insights,
        "key_factors": [
            f"Experience Level: {experience_years} years positions you in {'senior' if experience_years >= 5 else 'mid-level' if experience_years >= 2 else 'entry-level'} bracket",
            f"Location Factor: {location} has {'high' if 'india' not in location.lower() or 'bangalore' in location.lower() or 'mumbai' in location.lower() else 'moderate'} cost of living",
            f"Skill Premium: {_calculate_skill_premium(skills)} of your skills are in high demand",
            f"Market Demand: {'Strong' if experience_years >= 3 else 'Growing'} hiring activity for {job_title}",
            "Total Compensation: Base salary + bonuses + equity + benefits typically 20-40% above base"
        ]
    }


def _get_industry_insights(job_title: str, location: str, experience_years: int, currency_symbol: str) -> Dict:
    """Generate AI-powered industry-specific insights"""
    
    prompt = f"""As a compensation analyst, provide brief market insights for {job_title} with {experience_years} years experience in {location}:

1. Average salary increase year-over-year (%)
2. Top 3 companies hiring for this role in {location}
3. Demand trend (Growing/Stable/Declining)
4. One key negotiation leverage point

Keep it factual and concise (80 words max)."""
    
    insights_text = ai_service.generate_completion(prompt, max_tokens=300, temperature=0.6)
    
    return {
        "market_trends": insights_text,
        "confidence_level": "High" if experience_years >= 2 else "Moderate"
    }


def _calculate_skill_premium(skills: list) -> str:
    """Calculate what percentage of skills are high-demand"""
    if not skills:
        return "0%"
    
    high_demand_skills = {
        "python", "react", "aws", "kubernetes", "docker", "machine learning", 
        "deep learning", "tensorflow", "pytorch", "node.js", "typescript",
        "sql", "nosql", "microservices", "system design", "devops", "ci/cd",
        "nlp", "computer vision", "llm", "gpt", "langchain", "ai"
    }
    
    matching = sum(1 for skill in skills if any(hd in skill.lower() for hd in high_demand_skills))
    percentage = (matching / len(skills)) * 100 if skills else 0
    
    return f"{int(percentage)}%"


def estimate_salary(job_title: str, experience_years: int, location: str = "United States") -> Dict:
    """Estimate salary range based on job title, experience, and location"""
    
    # Base salary ranges (USD for US, INR for India)
    us_salary_data = {
        "data scientist": {"base": 85000, "per_year": 8000},
        "ml engineer": {"base": 90000, "per_year": 9000},
        "machine learning engineer": {"base": 90000, "per_year": 9000},
        "ai engineer": {"base": 88000, "per_year": 8500},
        "backend developer": {"base": 75000, "per_year": 7000},
        "backend engineer": {"base": 75000, "per_year": 7000},
        "frontend developer": {"base": 70000, "per_year": 6500},
        "frontend engineer": {"base": 70000, "per_year": 6500},
        "full stack developer": {"base": 80000, "per_year": 7500},
        "full stack engineer": {"base": 80000, "per_year": 7500},
        "software engineer": {"base": 75000, "per_year": 7000},
        "software developer": {"base": 72000, "per_year": 6800},
        "devops engineer": {"base": 85000, "per_year": 8000},
        "data analyst": {"base": 65000, "per_year": 5500},
        "data engineer": {"base": 82000, "per_year": 7500},
        "product manager": {"base": 90000, "per_year": 9000},
        "project manager": {"base": 75000, "per_year": 6500},
    }
    
    # India salary data (in INR)
    india_salary_data = {
        "data scientist": {"base": 1200000, "per_year": 150000},  # ~$14.4K - $19.2K
        "ml engineer": {"base": 1400000, "per_year": 180000},  # ~$16.8K - $23.8K
        "machine learning engineer": {"base": 1400000, "per_year": 180000},
        "ai engineer": {"base": 1350000, "per_year": 170000},  # ~$16.2K - $22.8K
        "backend developer": {"base": 900000, "per_year": 120000},  # ~$10.8K - $14.4K
        "backend engineer": {"base": 900000, "per_year": 120000},
        "frontend developer": {"base": 850000, "per_year": 110000},  # ~$10.2K - $13.2K
        "frontend engineer": {"base": 850000, "per_year": 110000},
        "full stack developer": {"base": 1000000, "per_year": 130000},  # ~$12K - $16.6K
        "full stack engineer": {"base": 1000000, "per_year": 130000},
        "software engineer": {"base": 900000, "per_year": 120000},  # ~$10.8K - $14.4K
        "software developer": {"base": 850000, "per_year": 110000},  # ~$10.2K - $13.2K
        "devops engineer": {"base": 1100000, "per_year": 140000},  # ~$13.2K - $17.8K
        "data analyst": {"base": 700000, "per_year": 90000},  # ~$8.4K - $10.8K
        "data engineer": {"base": 1050000, "per_year": 130000},  # ~$12.6K - $16.6K
        "product manager": {"base": 1300000, "per_year": 160000},  # ~$15.6K - $21.6K
        "project manager": {"base": 950000, "per_year": 120000},  # ~$11.4K - $15.0K
    }
    
    # Choose dataset based on location
    is_india = "india" in location.lower()
    salary_data = india_salary_data if is_india else us_salary_data
    
    # Find matching role
    title_lower = job_title.lower()
    role_data = None
    
    for role, data in salary_data.items():
        if role in title_lower:
            role_data = data
            break
    
    # Default if role not found
    if not role_data:
        if is_india:
            role_data = {"base": 800000, "per_year": 100000}  # ~$9.6K - $10K per year
        else:
            role_data = {"base": 70000, "per_year": 6500}
    
    # Calculate based on experience
    base_salary = role_data["base"]
    annual_increase = role_data["per_year"]
    
    # Cap experience at 10 years for calculation
    effective_years = min(experience_years, 10)
    
    estimated = base_salary + (annual_increase * effective_years)
    
    return {
        "min": int(estimated * 0.85),
        "target": int(estimated),
        "max": int(estimated * 1.20),
        "currency": "INR" if is_india else "USD"
    }


def generate_negotiation_email(
    current_offer: int,
    desired_salary: int,
    justification: str
) -> str:
    """Generate a professional salary negotiation email"""
    
    prompt = f"""Write a professional salary negotiation email:

Current Offer: ${current_offer:,}
Desired Salary: ${desired_salary:,}
Justification: {justification}

Requirements:
- Be professional and grateful
- Reference the current offer
- Provide data-backed justification
- Express enthusiasm for the role
- Suggest a specific counteroffer
- Keep it concise (150-200 words)

Email:"""
    
    return ai_service.generate_completion(prompt, max_tokens=500)


def compare_offers(offers: list) -> Dict:
    """Compare multiple job offers"""
    
    if not offers:
        return {"error": "No offers provided"}
    
    comparison = {
        "highest_salary": max(offers, key=lambda x: x.get('salary', 0)),
        "analysis": []
    }
    
    for offer in offers:
        score = calculate_offer_score(offer)
        comparison["analysis"].append({
            "company": offer.get("company", "Unknown"),
            "salary": offer.get("salary", 0),
            "score": score,
            "pros": offer.get("pros", []),
            "cons": offer.get("cons", [])
        })
    
    # Sort by score
    comparison["analysis"].sort(key=lambda x: x["score"], reverse=True)
    comparison["recommended"] = comparison["analysis"][0] if comparison["analysis"] else None
    
    return comparison


def calculate_offer_score(offer: Dict) -> float:
    """Calculate a score for a job offer"""
    score = 0
    
    # Salary weight: 40%
    salary = offer.get("salary", 0)
    score += (salary / 1000) * 0.4
    
    # Benefits weight: 20%
    benefits = offer.get("benefits_score", 5)  # 0-10 scale
    score += benefits * 2
    
    # Growth weight: 20%
    growth = offer.get("growth_potential", 5)  # 0-10 scale
    score += growth * 2
    
    # Culture weight: 20%
    culture = offer.get("culture_fit", 5)  # 0-10 scale
    score += culture * 2
    
    return round(score, 2)
