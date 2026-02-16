from .ai_service import ai_service
from typing import List, Dict

def generate_interview_questions(job_title: str, job_description: str, skills: List[str]) -> Dict:
    """Generate highly specific, role-tailored interview questions with real scenarios"""
    
    # Enhanced AI prompt for more realistic, targeted questions
    prompt = f"""You are a senior technical interviewer with 10+ years of experience hiring for {job_title} positions. Generate highly specific, realistic interview questions that actual companies ask for this role.

**Job Role Analysis:**
- Position: {job_title}
- Required Skills: {', '.join(skills[:10])}
- Job Context (truncated): {job_description[:500]}

**Generate Interview Questions:**

**TECHNICAL QUESTIONS** (5 questions):
Generate role-specific technical questions that test deep understanding, not just theory.
- For coding roles: Include algorithm problems, system design, debugging scenarios
- For data roles: Include case studies, model selection, data pipeline questions  
- For ML/AI roles: Include model evaluation, deployment, bias/fairness questions
- Make questions realistic and scenario-based (e.g., "You have 100M records...")

**BEHAVIORAL QUESTIONS** (5 questions):
Generate questions using STAR method that reveal:
- Leadership and teamwork capabilities
- Problem-solving under pressure
- Conflict resolution
- Project failures and learnings
- Career motivations and long-term goals
Examples: "Tell me about a time when...", "Describe a situation where..."

**QUESTIONS CANDIDATE SHOULD ASK** (3 questions):
Generate thoughtful questions that show:
- Technical curiosity about the role
- Interest in team dynamics and growth
- Understanding of business impact
Examples focusing on: tech stack, team structure, success metrics, challenges

**Format each section clearly as:**
TECHNICAL QUESTIONS:
1. [Specific scenario-based question]
2. [Question]
...

BEHAVIORAL QUESTIONS:
1. [STAR-format question]
2. [Question]
...

QUESTIONS TO ASK:
1. [Insightful question]
2. [Question]
...

Make questions challenging but fair. Avoid generic questions. Be specific to {job_title} role."""
    
    response = ai_service.generate_completion(prompt, max_tokens=1500, temperature=0.7)
    
    # Generate answer frameworks for top technical questions
    technical_questions = _extract_questions(response, "TECHNICAL")
    sample_frameworks = {}
    
    if technical_questions:
        # Get framework for first technical question
        framework_prompt = f"""Provide a concise answer framework for this {job_title} interview question:

Question: {technical_questions[0]}

Give:
1. Key approach/methodology (2-3 sentences)
2. Main points to cover (3-4 bullet points)
3. One tip for strong delivery

Keep it brief (100 words max)."""
        
        sample_frameworks["first_technical"] = ai_service.generate_completion(framework_prompt, max_tokens=300)
    
    # Parse response into structured format
    return {
        "technical_questions": technical_questions,
        "behavioral_questions": _extract_questions(response, "BEHAVIORAL"),
        "questions_to_ask": _extract_questions(response, "QUESTIONS TO ASK"),
        "sample_framework": sample_frameworks.get("first_technical", ""),
        "full_response": response
    }


def generate_interview_tips(job_title: str, company_name: str = "") -> str:
    """Generate comprehensive interview preparation tips with company-specific insights"""
    
    prompt = f"""You are an executive interview coach. Provide detailed, actionable interview preparation tips for a {job_title} position{f' at {company_name}' if company_name else ''}.

**Preparation Roadmap:**

1. **Pre-Interview Research** (5 specific actions):
   - What to research about {"the company" if company_name else "typical companies hiring for this role"}
   - Key technologies/methodologies to review for {job_title}
   - Common interview formats for this role (technical screens, system design, behavioral rounds)
   - Questions to prepare based on role seniority
   
2. **Day-of Interview Strategy** (4-5 tactical tips):
   - How to structure technical answers (e.g., clarify requirements, discuss trade-offs)
   - Body language and communication techniques
   - How to handle questions you don't know
   - Building rapport with interviewers

3. **Common Mistakes to Avoid** (4 specific pitfalls):
   - Technical communication errors (e.g., jumping to code without clarifying requirements)
   - Behavioral interview mistakes (vague answers, no metrics)
   - Red flag behaviors that make hiring managers hesitate
   
4. **What Interviewers Look For** in {job_title} candidates:
   - Technical competency indicators
   - Problem-solving approach and thought process
   - Communication and collaboration signals
   - Cultural fit and growth mindset indicators

5. **Making a Lasting Impression** (3-4 strategies):
   - How to showcase unique value beyond technical skills
   - Smart follow-up strategies (thank you notes, additional portfolio items)
   - Building relationships for future opportunities

Provide specific, realistic advice that goes beyond generic tips. Include examples and exact phrases where helpful. (400-500 words total)"""
    
    return ai_service.generate_completion(prompt, max_tokens=1200, temperature=0.7)


def generate_answer_framework(question: str, job_context: str) -> str:
    """Generate a detailed framework for answering specific interview questions with examples"""
    
    prompt = f"""You are an interview coach. Help a candidate structure a strong answer for this interview question.

**Interview Question:** {question}

**Job Context:** {job_context}

**Provide a comprehensive answer framework:**

1. **Answer Structure**:
   - Identify if this needs STAR method (Situation, Task, Action, Result) or another framework
   - Outline the logical flow of a strong answer
   - Recommended time to spend on each part (e.g., 30 seconds on situation, 1 minute on action)

2. **Key Points to Cover** (5-7 specific elements):
   - Technical details to mention (if applicable)
   - Metrics or quantifiable results to include
   - Skills or competencies to demonstrate
   - Common pitfalls to avoid for this specific question

3. **Example Answer Outline**:
   - Write a 3-4 sentence skeleton showing how to structure the response
   - Use [brackets] for parts they should personalize
   - Include transition phrases

4. **Delivery Tips** (2-3 tactical points):
   - How to maintain confidence and clarity
   - When to pause for questions
   - How to show enthusiasm while staying professional

Make this highly actionable and specific to the question asked. (250-300 words)"""
    
    return ai_service.generate_completion(prompt, max_tokens=800, temperature=0.7)


def _extract_questions(text: str, section: str) -> List[str]:
    """Extract questions from formatted text"""
    questions = []
    lines = text.split('\n')
    in_section = False
    
    for line in lines:
        if section in line.upper():
            in_section = True
            continue
        
        if in_section:
            # Stop at next section
            if any(keyword in line.upper() for keyword in ["TECHNICAL", "BEHAVIORAL", "QUESTIONS TO ASK"]) and section not in line.upper():
                break
            
            # Extract numbered questions
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                # Remove numbering
                question = line.lstrip('0123456789.-•) ').strip()
                if question:
                    questions.append(question)
    
    return questions[:10]  # Limit to 10 questions per section
