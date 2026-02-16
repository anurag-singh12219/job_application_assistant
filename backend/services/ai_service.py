import os
from typing import List, Dict, Optional
import requests
import json
from dotenv import load_dotenv
from pathlib import Path

# Load .env from backend directory explicitly
env_path = Path(__file__).parent.parent / ".env"
print(f"[AI Service Init] Loading .env from: {env_path}")
load_dotenv(dotenv_path=env_path, override=True)

class AIService:
    """AI Service using Groq/OpenAI for advanced features"""
    
    def __init__(self):
        # Get and trim API key
        groq_key = os.getenv("GROQ_API_KEY", "").strip()
        openai_key = os.getenv("OPENAI_API_KEY", "").strip()
        
        self.api_key = groq_key or openai_key
        self.use_groq = bool(groq_key)
        
        # Debug logging
        if self.api_key:
            print(f"[AI Service] ✓ API Key loaded successfully ({len(self.api_key)} chars, using {'Groq' if self.use_groq else 'OpenAI'})")
        else:
            print(f"[AI Service] ⚠ No API key found in environment")
            print(f"[AI Service] GROQ_API_KEY={groq_key[:20] if groq_key else 'NOT SET'}")
            print(f"[AI Service] OPENAI_API_KEY={openai_key[:20] if openai_key else 'NOT SET'}")
        
        if self.use_groq:
            self.api_url = "https://api.groq.com/openai/v1/chat/completions"
            self.model = "llama-3.1-8b-instant"
        else:
            self.api_url = "https://api.openai.com/v1/chat/completions"
            self.model = "gpt-3.5-turbo"
    
    def generate_completion(self, prompt: str, max_tokens: int = 1500, temperature: float = 0.7, system_message: Optional[str] = None) -> str:
        """Generate AI completion with enhanced parameters"""
        if not self.api_key:
            error_msg = "⚠ No API key configured. Add GROQ_API_KEY or OPENAI_API_KEY to .env file"
            print(f"[AI Service] {error_msg}")
            return self._get_context_aware_response(prompt)
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})
            
            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            print(f"[AI Service] Calling {self.model} API at {self.api_url[:40]}...")
            response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
            
            print(f"[AI Service] Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()["choices"][0]["message"]["content"]
                print(f"[AI Service] ✓ Success: {len(result)} characters received")
                return result
            elif response.status_code == 401:
                error_msg = f"❌ Authentication failed (401). Check your API key in .env"
                print(f"[AI Service] {error_msg}")
                print(f"[AI Service] Response: {response.text[:200]}")
                return self._get_context_aware_response(prompt)
            elif response.status_code == 429:
                error_msg = f"⏱ Rate limit exceeded (429). Please try again later"
                print(f"[AI Service] {error_msg}")
                return self._get_context_aware_response(prompt)
            else:
                error_msg = f"API Error: Status {response.status_code}"
                print(f"[AI Service] {error_msg}")
                print(f"[AI Service] Response: {response.text[:300]}")
                return self._get_context_aware_response(prompt)
        except requests.exceptions.Timeout:
            error_msg = "⏱ API request timed out. Please try again"
            print(f"[AI Service] {error_msg}")
            return self._get_context_aware_response(prompt)
        except requests.exceptions.ConnectionError:
            error_msg = "🌐 Connection error. Check your internet connection"
            print(f"[AI Service] {error_msg}")
            return self._get_context_aware_response(prompt)
        except Exception as e:
            error_msg = f"❌ Error: {type(e).__name__}: {str(e)}"
            print(f"[AI Service] {error_msg}")
            return self._get_context_aware_response(prompt)
    
    def _get_context_aware_response(self, prompt: str) -> str:
        """Return context-aware response based on what user is asking"""
        lower_prompt = prompt.lower()
        
        if "cover letter" in lower_prompt:
            return self._generate_cover_letter_template()
        elif "interview" in lower_prompt:
            return self._generate_interview_tips()
        elif "salary" in lower_prompt or "negotiate" in lower_prompt:
            return self._generate_salary_tips()
        elif "resume" in lower_prompt or "cv" in lower_prompt:
            return self._generate_resume_feedback()
        elif "skill" in lower_prompt or "learn" in lower_prompt:
            return self._generate_skill_development_tips()
        else:
            return self._get_general_career_advice()
    
    def _get_general_career_advice(self) -> str:
        return """I'm here to help you navigate your career journey! I can assist with:

📄 **Resumes** - Optimization, ATS tips, tailoring advice
💬 **Interviews** - Practice questions, STAR method, preparation strategies  
💰 **Salary** - Market research, negotiation tactics, offer evaluation
✍️ **Cover Letters** - Writing tips, examples, customization
🎯 **Job Search** - Strategy, networking, application tips
🎓 **Skills Development** - Learning paths, certifications, growth strategies

What aspect of your career would you like to focus on?"""
    
    def _generate_cover_letter_template(self) -> str:
        return """Dear Hiring Manager,

I am writing to express my strong interest in the [Position] role at [Company]. With my background in [Your Field] and proven track record in [Key Skills], I am confident in my ability to contribute to your team's success.

In my previous role, I successfully [Achievement 1] and [Achievement 2], demonstrating my ability to [Key Competency]. My experience with [Relevant Skills] aligns perfectly with the requirements outlined in your job posting.

I am particularly drawn to [Company] because of [Specific Reason About Company]. I am excited about the opportunity to bring my expertise in [Your Strengths] to help achieve [Company Goals].

I would welcome the opportunity to discuss how my skills and experience can benefit your team. Thank you for considering my application.

Best regards,
[Your Name]"""
    
    def _generate_interview_tips(self) -> str:
        return """**Interview Preparation Tips:**

1. **Research the Company**: Understand their products, culture, and recent news
2. **Practice STAR Method**: Structure answers with Situation, Task, Action, Result
3. **Prepare Questions**: Have 3-5 thoughtful questions ready
4. **Review Your Resume**: Be ready to discuss every point
5. **Technical Preparation**: Practice coding/technical questions if applicable
6. **Dress Appropriately**: Professional attire suitable for the company culture
7. **Follow Up**: Send a thank-you email within 24 hours"""
    
    def _generate_salary_tips(self) -> str:
        return """**Salary Negotiation Strategy:**

1. **Research Market Rates**: Use sites like Glassdoor, LinkedIn, Payscale
2. **Know Your Worth**: Consider your experience, skills, and location
3. **Wait for the Offer**: Let them make the first offer
4. **Consider Total Compensation**: Benefits, bonuses, equity, work-life balance
5. **Be Professional**: Use collaborative language, not confrontational
6. **Have a Range**: Know your minimum, target, and ideal salary
7. **Practice Your Pitch**: Rehearse discussing your value proposition"""
    
    def _generate_resume_feedback(self) -> str:
        return """**Resume Enhancement Tips:**

1. **Quantify Achievements**: Use numbers and metrics
2. **Action Verbs**: Start bullets with strong action verbs
3. **Tailor Content**: Customize for each job application
4. **Keep It Concise**: 1-2 pages maximum
5. **Format Consistently**: Use clear hierarchy and spacing
6. **Highlight Impact**: Focus on results, not just responsibilities
7. **Proofread**: Eliminate all typos and grammatical errors"""
    
    def _generate_skill_development_tips(self) -> str:
        return """**Skills Development Roadmap:**

1. **Identify High-Demand Skills**: Check job postings in your target role
2. **Create Learning Plan**: Plan 3-6 month learning journey  
3. **Choose Resources**: Use Coursera, Udemy, LinkedIn Learning, YouTube
4. **Build Projects**: Apply skills in real-world projects
5. **Join Communities**: Network on Reddit, Discord, GitHub
6. **Get Certified**: Earn recognized certifications
7. **Contribute to Open Source**: Build portfolio on GitHub

Remember: Consistency beats intensity. Spend 1-2 hours daily for steady progress!"""
# Global AI service instance
ai_service = AIService()