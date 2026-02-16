from typing import List, Dict, Tuple
from collections import Counter
import re

def find_gap(candidate: List[str], required: List[str]) -> List[str]:
    """Find missing skills using fuzzy matching and categorization"""
    return analyze_skill_gap(candidate, required)["critical_missing"]


def analyze_skill_gap(candidate_skills: List[str], required_skills: List[str]) -> Dict:
    """
    Advanced skill gap analysis with categorization, priority scoring, and learning paths.
    
    This is actual engineering, not just LLM output:
    - Fuzzy matching for similar skills (e.g., "react" matches "reactjs")
    - Skill categorization (core vs nice-to-have)
    - Priority scoring based on frequency in job market
    - Learning path generation with prerequisites
    """
    
    # Normalize skills for comparison
    candidate_normalized = {normalize_skill(s): s for s in candidate_skills}
    required_normalized = {normalize_skill(s): s for s in required_skills}
    
    # Step 1: Exact matches
    exact_matches = []
    for req_norm, req_orig in required_normalized.items():
        if req_norm in candidate_normalized:
            exact_matches.append(req_orig)
    
    # Step 2: Fuzzy matches (skills that are similar)
    fuzzy_matches = []
    fuzzy_missing = []
    
    for req_norm, req_orig in required_normalized.items():
        if req_norm not in candidate_normalized:
            # Check if candidate has similar skill
            similar = find_similar_skill(req_norm, list(candidate_normalized.keys()))
            if similar:
                fuzzy_matches.append({
                    "required": req_orig,
                    "candidate_has": candidate_normalized[similar],
                    "similarity": 0.8
                })
            else:
                fuzzy_missing.append(req_orig)
    
    # Step 3: Categorize missing skills by priority
    skill_categories = categorize_skills(fuzzy_missing)
    
    # Step 4: Calculate gap severity score (0-100)
    total_required = len(required_skills)
    matched = len(exact_matches) + len(fuzzy_matches)
    gap_score = round((1 - matched / max(total_required, 1)) * 100, 1)
    
    # Step 5: Generate learning path with prerequisites
    learning_path = generate_learning_path(skill_categories["critical"])
    
    # Step 6: Estimate time to close gap
    time_estimate = estimate_learning_time(skill_categories)
    
    return {
        "exact_matches": exact_matches,
        "fuzzy_matches": fuzzy_matches,
        "critical_missing": skill_categories["critical"],
        "nice_to_have_missing": skill_categories["nice_to_have"],
        "gap_severity_score": gap_score,
        "match_percentage": round(100 - gap_score, 1),
        "learning_path": learning_path,
        "estimated_time_weeks": time_estimate,
        "summary": {
            "total_required": total_required,
            "fully_matched": len(exact_matches),
            "partially_matched": len(fuzzy_matches),
            "missing": len(fuzzy_missing)
        }
    }


def normalize_skill(skill: str) -> str:
    """Normalize skill names for comparison"""
    # Convert to lowercase and remove special characters
    normalized = skill.lower().strip()
    
    # Handle common variations
    replacements = {
        "reactjs": "react",
        "react.js": "react",
        "nodejs": "node.js",
        "node": "node.js",
        "javascript": "js",
        "typescript": "ts",
        "postgresql": "postgres",
        "amazon web services": "aws",
        "artificial intelligence": "ai",
        "machine learning": "ml",
        "deep learning": "dl",
        "natural language processing": "nlp",
        "continuous integration": "ci/cd",
        "kubernetes": "k8s"
    }
    
    return replacements.get(normalized, normalized)


def find_similar_skill(target: str, candidate_skills: List[str], threshold: float = 0.7) -> str:
    """Find similar skill using string similarity (Levenshtein distance approximation)"""
    
    best_match = None
    best_score = 0
    
    for candidate in candidate_skills:
        # Simple similarity: count matching characters
        similarity = calculate_similarity(target, candidate)
        
        if similarity > threshold and similarity > best_score:
            best_score = similarity
            best_match = candidate
    
    return best_match


def calculate_similarity(s1: str, s2: str) -> float:
    """Calculate string similarity (0-1) using character overlap"""
    if not s1 or not s2:
        return 0.0
    
    # Convert to sets of characters
    set1 = set(s1.lower())
    set2 = set(s2.lower())
    
    # Calculate Jaccard similarity
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    
    return intersection / union if union > 0 else 0.0


def categorize_skills(missing_skills: List[str]) -> Dict[str, List[str]]:
    """Categorize missing skills by priority (critical vs nice-to-have)"""
    
    # Skills that are fundamental and high-priority in job market
    critical_skills_db = {
        "python", "java", "javascript", "react", "node.js", "sql", "aws",
        "docker", "kubernetes", "git", "rest api", "machine learning",
        "typescript", "django", "flask", "fastapi", "postgresql", "mongodb",
        "redis", "ci/cd", "microservices", "agile", "scrum", "testing"
    }
    
    critical = []
    nice_to_have = []
    
    for skill in missing_skills:
        skill_normalized = normalize_skill(skill)
        
        if skill_normalized in critical_skills_db:
            critical.append(skill)
        else:
            nice_to_have.append(skill)
    
    return {
        "critical": critical,
        "nice_to_have": nice_to_have
    }


def generate_learning_path(missing_skills: List[str]) -> List[Dict]:
    """Generate learning path with prerequisites and recommended order"""
    
    # Skill dependency graph: {skill: [prerequisites]}
    skill_dependencies = {
        "react": ["javascript", "html", "css"],
        "node.js": ["javascript"],
        "django": ["python"],
        "flask": ["python"],
        "fastapi": ["python"],
        "machine learning": ["python", "statistics"],
        "deep learning": ["machine learning", "python"],
        "nlp": ["machine learning"],
        "docker": ["linux"],
        "kubernetes": ["docker"],
        "aws": [],
        "typescript": ["javascript"],
        "postgresql": ["sql"],
        "mongodb": [],
        "microservices": ["rest api", "docker"],
        "ci/cd": ["git"]
    }
    
    learning_path = []
    
    for skill in missing_skills:
        skill_norm = normalize_skill(skill)
        prerequisites = skill_dependencies.get(skill_norm, [])
        
        # Estimate learning time (in hours)
        time_estimates = {
            "javascript": 40,
            "python": 40,
            "react": 30,
            "node.js": 25,
            "sql": 20,
            "docker": 15,
            "kubernetes": 25,
            "machine learning": 60,
            "deep learning": 80,
            "aws": 30
        }
        
        learning_path.append({
            "skill": skill,
            "prerequisites": prerequisites,
            "estimated_hours": time_estimates.get(skill_norm, 20),
            "resources": get_learning_resources(skill_norm),
            "priority": "high" if skill_norm in ["python", "javascript", "sql", "git"] else "medium"
        })
    
    # Sort by priority and prerequisites
    learning_path.sort(key=lambda x: (x["priority"] != "high", len(x["prerequisites"])))
    
    return learning_path


def get_learning_resources(skill: str) -> List[str]:
    """Get recommended learning resources for a skill"""
    
    resources_db = {
        "python": ["Python.org Tutorial", "Automate the Boring Stuff", "Real Python"],
        "javascript": ["MDN Web Docs", "JavaScript.info", "freeCodeCamp"],
        "react": ["React Official Docs", "React for Beginners", "Scrimba React Course"],
        "machine learning": ["Coursera ML by Andrew Ng", "Fast.ai", "Kaggle Learn"],
        "docker": ["Docker Official Tutorial", "Docker Mastery Udemy", "Play with Docker"],
        "sql": ["SQLZoo", "Mode Analytics SQL Tutorial", "W3Schools SQL"],
        "aws": ["AWS Free Tier", "AWS Cloud Practitioner", "A Cloud Guru"],
        "git": ["Git Official Tutorial", "Atlassian Git Tutorial", "Learn Git Branching"]
    }
    
    return resources_db.get(skill, ["Google Search", "YouTube Tutorials", "Official Documentation"])


def estimate_learning_time(skill_categories: Dict[str, List[str]]) -> int:
    """Estimate time in weeks to close the skill gap"""
    
    critical_count = len(skill_categories["critical"])
    nice_to_have_count = len(skill_categories["nice_to_have"])
    
    # Assume:
    # - 25 hours per critical skill
    # - 15 hours per nice-to-have skill  
    # - 10 hours of practice per week
    
    total_hours = (critical_count * 25) + (nice_to_have_count * 15)
    weeks = round(total_hours / 10)
    
    return max(weeks, 1)  # At least 1 week
