from .ai_service import ai_service

PLACEHOLDER_TOKENS = [
    "[Position]",
    "[Company]",
    "[Your Name]",
    "[Key Skills]",
    "[Your Field]",
    "[Achievement",
    "[Relevant Skills]",
    "[Company Goals]",
    "[Your Strengths]",
    "[Specific Reason"
]


def _contains_placeholders(text: str) -> bool:
    return any(token in text for token in PLACEHOLDER_TOKENS)


def _basic_cover_letter(
    user_name: str,
    job_title: str,
    company_name: str,
    skills: list,
    experience_years: int,
    tone: str
) -> str:
    name = user_name or "Candidate"
    role = job_title or "the role"
    company = company_name or "the company"
    skills_text = ", ".join([s for s in skills if s][:6]) or "relevant technical skills"
    exp_text = (
        f"with {experience_years} years of experience" if experience_years
        else "as an early-career professional"
    )

    return f"""Dear Hiring Manager,

I am excited to apply for the {role} position at {company}. {exp_text}, I have built a strong foundation in {skills_text}. I am especially interested in {company} because of its focus on impact and innovation, and I am eager to contribute to your team.

In recent projects, I have applied {skills_text} to solve real problems, improve quality, and collaborate across teams. I enjoy translating requirements into clean, reliable solutions and continuously learning to stay current with industry best practices.

I would welcome the opportunity to discuss how my background aligns with your needs. Thank you for your time and consideration.

Best regards,
{name}
"""

def generate_cover_letter(
    job_title: str,
    company_name: str,
    job_description: str,
    resume_text: str,
    skills: list,
    tone: str = "professional"
) -> str:
    """Generate a personalized cover letter using AI"""
    
    prompt = f"""Generate a professional, human-sounding cover letter for the following:

Job Title: {job_title}
Company: {company_name}

Job Description:
{job_description[:500]}

Candidate's Key Skills: {', '.join(skills)}

Tone: {tone}

Requirements:
- Write a compelling cover letter (250-300 words)
- Use ONLY the provided data; do NOT include placeholders or brackets
- Mention the company and role explicitly
- Highlight relevant skills and experience
- Show enthusiasm for the role and company
- Use professional language
- Include specific examples where possible
- Make it personalized and genuine

Generate the cover letter:"""
    
    response = ai_service.generate_completion(
        prompt,
        max_tokens=800,
        temperature=0.6,
        system_message="You write concise, realistic cover letters. Never use placeholders or bracketed text."
    )

    if _contains_placeholders(response):
        response = ai_service.generate_completion(
            prompt + "\n\nImportant: Do not use placeholders like [Position] or [Company].",
            max_tokens=800,
            temperature=0.5,
            system_message="Return a final, ready-to-send cover letter without placeholders."
        )

    if _contains_placeholders(response):
        response = _basic_cover_letter("Candidate", job_title, company_name, skills, 0, tone)

    return response


def generate_custom_cover_letter(
    user_name: str,
    job_title: str,
    company_name: str,
    skills: list,
    experience_years: int
) -> str:
    """Generate a quick custom cover letter"""
    
    prompt = f"""Write a professional, human-sounding cover letter for:

Candidate: {user_name}
Position: {job_title}
Company: {company_name}
Key Skills: {', '.join(skills[:5])}
Experience: {experience_years} years

Make it concise (200-250 words), professional, and impactful.
Do NOT use placeholders or brackets. Use the provided data.

Cover Letter:"""
    
    response = ai_service.generate_completion(
        prompt,
        max_tokens=600,
        temperature=0.6,
        system_message="Return a final cover letter using the provided details. Avoid placeholders."
    )

    if _contains_placeholders(response):
        response = ai_service.generate_completion(
            prompt + "\n\nImportant: Do not use placeholders like [Company] or [Your Name].",
            max_tokens=600,
            temperature=0.5,
            system_message="Return a final, ready-to-send cover letter without placeholders."
        )

    if _contains_placeholders(response):
        response = _basic_cover_letter(user_name, job_title, company_name, skills, experience_years, "professional")

    return response
