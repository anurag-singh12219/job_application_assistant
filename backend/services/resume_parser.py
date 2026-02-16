import pdfplumber
import spacy
import re
from typing import List, Dict

nlp = spacy.load("en_core_web_sm")

# Comprehensive skills database
SKILLS_DB = [
    # Programming Languages
    "python", "java", "javascript", "typescript", "c", "c++", "c#", "ruby", "php", "swift", "kotlin", "go", "rust", "scala", "r",
    
    # Web Technologies
    "html", "css", "react", "angular", "vue", "node.js", "express", "django", "flask", "fastapi", "spring", "asp.net", "jquery", 
    "bootstrap", "tailwind", "next.js", "nuxt", "svelte", "webpack", "vite",
    
    # Databases
    "sql", "mysql", "postgresql", "mongodb", "redis", "cassandra", "dynamodb", "oracle", "sqlite", "elasticsearch", "neo4j",
    
    # Cloud & DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "gitlab", "github actions", "terraform", "ansible", "ci/cd", 
    "linux", "unix", "bash", "nginx", "apache",
    
    # Data Science & AI
    "machine learning", "deep learning", "nlp", "computer vision", "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", 
    "numpy", "matplotlib", "seaborn", "jupyter", "statistics", "data analysis", "data visualization", "ml", "dl", "ai",
    
    # Mobile Development
    "android", "ios", "react native", "flutter", "xamarin", "mobile development",
    
    # Testing & Quality
    "testing", "unit testing", "integration testing", "jest", "pytest", "selenium", "cypress", "testing",
    
    # Other Technologies
    "git", "rest api", "graphql", "microservices", "agile", "scrum", "jira", "api", "json", "xml",
    "security", "authentication", "oauth", "jwt", "encryption"
]

def extract_text(file):
    """Extract text from PDF file"""
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
    return text


def extract_skills(text: str) -> List[str]:
    """Extract skills from text using NLP and pattern matching"""
    text_lower = text.lower()
    found_skills = set()
    
    # Method 1: Direct keyword matching
    for skill in SKILLS_DB:
        if skill in text_lower:
            found_skills.add(skill)
    
    # Method 2: NLP entity extraction
    doc = nlp(text_lower)
    for token in doc:
        if token.text in SKILLS_DB:
            found_skills.add(token.text)
    
    return sorted(list(found_skills))


def extract_contact_info(text: str) -> Dict[str, str]:
    """Extract contact information from resume"""
    contact_info = {
        "email": "",
        "phone": "",
        "linkedin": "",
        "github": ""
    }
    
    # Extract email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    if emails:
        contact_info["email"] = emails[0]
    
    # Extract phone
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    phones = re.findall(phone_pattern, text)
    if phones:
        contact_info["phone"] = phones[0] if isinstance(phones[0], str) else phones[0][0]
    
    # Extract LinkedIn
    linkedin_pattern = r'linkedin\.com/in/([\w-]+)'
    linkedin = re.search(linkedin_pattern, text, re.IGNORECASE)
    if linkedin:
        contact_info["linkedin"] = f"linkedin.com/in/{linkedin.group(1)}"
    
    # Extract GitHub
    github_pattern = r'github\.com/([\w-]+)'
    github = re.search(github_pattern, text, re.IGNORECASE)
    if github:
        contact_info["github"] = f"github.com/{github.group(1)}"
    
    return contact_info


def extract_experience_years(text: str) -> float:
    """Estimate years of experience from resume"""
    # Look for date patterns
    year_patterns = r'(20\d{2})|(19\d{2})'
    years = re.findall(year_patterns, text)
    
    unique_years = set()
    for year_tuple in years:
        for year in year_tuple:
            if year:
                unique_years.add(int(year))
    
    if len(unique_years) >= 2:
        return max(unique_years) - min(unique_years)
    
    # Look for explicit experience mentions
    exp_pattern = r'(\d+)\+?\s*years?\s*(of)?\s*experience'
    exp_match = re.search(exp_pattern, text, re.IGNORECASE)
    if exp_match:
        return float(exp_match.group(1))
    
    return 0.0
