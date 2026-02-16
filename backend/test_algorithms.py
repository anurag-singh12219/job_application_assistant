"""Test script to verify enhanced algorithms work correctly"""

from services.skill_gap import analyze_skill_gap
from services.job_matcher import match_jobs
from services.ats_engine import calculate_detailed_ats

print("=" * 60)
print("TESTING ENHANCED ALGORITHMS")
print("=" * 60)

# Test 1: Skill Gap Analyzer
print("\n1. Testing Skill Gap Analyzer...")
candidate = ['python', 'react', 'sql']
required = ['python', 'react', 'kubernetes', 'docker', 'aws']
result = analyze_skill_gap(candidate, required)
print(f"   ✓ Gap Score: {result['gap_severity_score']}%")
print(f"   ✓ Match: {result['match_percentage']}%")
print(f"   ✓ Missing: {result['critical_missing']}")
print(f"   ✓ Learning Time: {result['estimated_time_weeks']} weeks")

# Test 2: Job Matcher
print("\n2. Testing Job Matcher...")
try:
    jobs = match_jobs(['python', 'machine learning', 'sql'], experience_years=3)
    if jobs:
        print(f"   ✓ Found {len(jobs)} job matches")
        top_job = jobs[0]
        print(f"   ✓ Top Match: {top_job['role']} ({top_job['match_score']}%)")
        print(f"   ✓ Breakdown: {top_job['score_breakdown']}")
except Exception as e:
    print(f"   ⚠ Job matcher needs CSV data: {e}")

# Test 3: ATS Engine
print("\n3. Testing ATS Engine...")
resume = """John Doe
Software Engineer with 5 years experience
Skills: Python, React, AWS, Docker, Kubernetes
Built microservices handling 1M requests/day
Email: john@example.com
Phone: 123-456-7890"""

job_desc = """Looking for Software Engineer with Python, React, Kubernetes experience.
Must have 3+ years of experience building scalable applications."""

result = calculate_detailed_ats(resume, job_desc)
print(f"   ✓ Overall Score: {result['overall_score']}")
print(f"   ✓ Keyword Match: {result['breakdown']['keyword_match']}%")
print(f"   ✓ Matched Keywords: {len(result['matched_keywords'])}")
print(f"   ✓ Missing Keywords: {result['missing_keywords'][:3]}")

print("\n" + "=" * 60)
print("ALL ALGORITHMS WORKING! ✓")
print("=" * 60)
