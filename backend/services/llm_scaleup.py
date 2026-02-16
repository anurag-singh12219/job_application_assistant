import requests
import os

API_KEY = os.getenv("SCALEUP_API_KEY")

def generate_feedback(skills, role, gap, ats):
    prompt = f"""
Candidate Skills: {skills}
Recommended Role: {role}
Missing Skills: {gap}
ATS Score: {ats}

Give a concise improvement roadmap.
"""

    res = requests.post(
        "https://api.scaleup.ai/v1/chat",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"message": prompt}
    )

    return res.json().get("response", "")
