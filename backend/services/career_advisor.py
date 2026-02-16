from .ai_service import ai_service
from .ats_engine import calculate_detailed_ats
import json

def generate_feedback(skills, role, missing_skills, ats_score, resume_text="", job_description=""):
    """Generate comprehensive, AI-powered career feedback with detailed ATS analysis"""
    
    # Get detailed ATS breakdown if resume and job description available
    detailed_ats = None
    if resume_text and job_description:
        detailed_ats = calculate_detailed_ats(resume_text, job_description)
        ats_score = detailed_ats["overall_score"]  # Use more accurate score
    
    # Create an enhanced, highly detailed prompt for AI
    prompt = f"""You are an expert career advisor and resume consultant with 15+ years of experience. Provide detailed, personalized, and actionable feedback.

**Candidate Profile:**
- Target Role: {role}
- ATS Score: {ats_score}/100 {'(Below Average ⚠️)' if ats_score < 65 else '(Good ✓)' if ats_score < 80 else '(Excellent ✓✓)'}
- Identified Skills ({len(skills)}): {', '.join(skills[:12]) if skills else 'None identified'}
- Missing Critical Skills: {', '.join(missing_skills[:8]) if missing_skills else 'None'}

**Detailed ATS Analysis:**
{f'''- Keyword Match: {detailed_ats["breakdown"]["keyword_match"]}%
- Content Relevance: {detailed_ats["breakdown"]["content_relevance"]}%
- Format Quality: {'Strong' if detailed_ats["format_analysis"]["has_sections"] else 'Needs Improvement'}
- Missing Keywords: {', '.join(detailed_ats["missing_keywords"][:8]) if detailed_ats and detailed_ats["missing_keywords"] else 'N/A'}
- Matched Keywords: {len(detailed_ats["matched_keywords"])} found''' if detailed_ats else 'Basic TF-IDF analysis only'}

**Job Description Context:**
{job_description[:600] if job_description else 'Not provided - using general analysis for ' + role}

**Resume Excerpt:**
{resume_text[:700] if resume_text else 'Not provided - analysis based on skills list only'}

**Provide comprehensive, specific analysis:**

1. **Overall Assessment** (3-4 sentences):
   - Honest evaluation of resume strength for {role} position
   - Current competitive positioning (entry/mid/senior level alignment)
   - Immediate impression the resume makes
   - One key strength and one critical gap

2. **Resume Strengths** (3-4 specific points):
   - Highlight actual strong points from their skills/experience
   - Call out any standout achievements or projects
   - Note what's working well in ATS optimization
   
3. **Critical Improvements Needed** (4-6 specific, actionable items):
   - Exact keywords to add and where (e.g., "Add 'microservices' to Technical Skills section")
   - Formatting changes for better ATS parsing
   - Content gaps affecting candidacy
   - How to better quantify achievements
   - Specific sections to expand or restructure
   
4. **Skill Development Roadmap for {role}** (structured plan):
   - Top 3 priority skills to learn immediately (with learning resources)
   - 2-3 complementary skills for career growth
   - Recommended certifications or courses
   - Timeline: what to learn in 30/60/90 days
   
5. **Action Plan - Next 7 Days** (7 specific, time-bound tasks):
   - Day 1: [Specific task]
   - Day 2: [Specific task]
   - Day 3-4: [Specific task]
   - Day 5-7: [Specific task]
   Each task should be concrete, measurable, and directly improve job prospects

6. **Interview Preparation Strategy** (3-4 tactical points):
   - How to discuss skill gaps honestly in interviews
   - Story angles to emphasize based on their background
   - Company types to target given current skill level

Be brutally honest but encouraging. Give SPECIFIC advice, not generic platitudes. Use actual data from their profile. If they're not ready for the role, say so and provide a realistic timeline. (600-800 words total)"""
    
    system_message = "You are a senior career advisor who has helped 500+ candidates land jobs at top tech companies. You give honest, data-driven feedback with specific action items. You balance being encouraging with being realistic about skill gaps and timelines."
    
    # Get AI-powered feedback
    ai_feedback = ai_service.generate_completion(
        prompt=prompt,
        max_tokens=2000,
        temperature=0.7,
        system_message=system_message
    )
    
    # If AI response is too short or generic, enhance it
    if len(ai_feedback) < 150:
        ai_feedback = generate_fallback_feedback(skills, role, missing_skills, ats_score)
    
    # Append detailed ATS recommendations if available
    if detailed_ats and detailed_ats.get("recommendations"):
        ai_feedback += "\n\n**ATS Optimization Checklist:**\n"
        for rec in detailed_ats["recommendations"][:8]:
            ai_feedback += f"- {rec}\n"
    
    return ai_feedback


def generate_fallback_feedback(skills, role, missing_skills, ats_score):
    """Generate enhanced fallback feedback when AI is unavailable"""
    feedback = []
    
    # Overall Assessment
    if ats_score >= 80:
        feedback.append("🎯 **Excellent Match!** Your resume demonstrates strong alignment with the target role. Your skills and experience are well-positioned for success.")
    elif ats_score >= 60:
        feedback.append("✅ **Good Foundation** Your resume shows promise, but strategic improvements will significantly boost your chances of getting interviews.")
    elif ats_score >= 40:
        feedback.append("⚠️ **Needs Enhancement** Your resume has potential but requires optimization to effectively compete for your target role.")
    else:
        feedback.append("🔧 **Requires Major Revision** Your resume needs substantial improvements to align with the role requirements and pass ATS screening.")
    
    # Strengths
    feedback.append("\n**Your Strengths:**")
    if len(skills) >= 8:
        feedback.append(f"- Diverse technical skill set with {len(skills)} identified competencies")
    if ats_score >= 60:
        feedback.append("- Strong keyword optimization for ATS systems")
    if skills:
        top_skills = skills[:3]
        feedback.append(f"- Proficiency in key technologies: {', '.join(top_skills)}")
    
    # Areas for Improvement
    feedback.append("\n**Areas for Improvement:**")
    if ats_score < 70:
        feedback.append("- Enhance keyword density by incorporating more role-specific terminology")
    if len(skills) < 6:
        feedback.append("- Expand your technical skills showcase with relevant technologies")
    if missing_skills:
        feedback.append(f"- Address skill gaps: {', '.join(missing_skills[:4])}")
    feedback.append("- Quantify achievements with metrics and concrete results")
    feedback.append("- Tailor resume content specifically for each application")
    
    # Role-Specific Guidance
    role_guidance = {
        "Data Scientist": {
            "skills": ["Python", "R", "SQL", "Machine Learning", "Statistics", "Data Visualization"],
            "projects": "Build end-to-end ML pipelines, create data dashboards, conduct A/B testing",
            "focus": "statistical analysis, predictive modeling, and data storytelling"
        },
        "ML Engineer": {
            "skills": ["Python", "TensorFlow", "PyTorch", "Docker", "Kubernetes", "MLOps"],
            "projects": "Deploy ML models at scale, implement CI/CD for ML, optimize model performance",
            "focus": "model deployment, infrastructure, and production systems"
        },
        "Backend Developer": {
            "skills": ["Python/Java", "REST APIs", "SQL", "Docker", "AWS/Azure", "Microservices"],
            "projects": "Build scalable APIs, implement database optimizations, design system architecture",
            "focus": "system design, API development, and cloud infrastructure"
        },
        "Frontend Developer": {
            "skills": ["React", "JavaScript", "TypeScript", "CSS", "HTML", "Responsive Design"],
            "projects": "Create responsive UIs, optimize performance, implement modern design patterns",
            "focus": "user experience, component architecture, and performance optimization"
        },
        "Full Stack Developer": {
            "skills": ["React", "Node.js", "Python", "SQL", "REST APIs", "Docker"],
            "projects": "Build complete web applications, integrate frontend with backend, deploy to cloud",
            "focus": "end-to-end development, system integration, and DevOps"
        },
        "AI Engineer": {
            "skills": ["Deep Learning", "NLP", "Computer Vision", "PyTorch", "TensorFlow", "Python"],
            "projects": "Develop AI applications, fine-tune LLMs, implement computer vision solutions",
            "focus": "applied AI, model development, and innovative solutions"
        }
    }
    
    feedback.append(f"\n**Recommended Skills for {role}:**")
    if role in role_guidance:
        guidance = role_guidance[role]
        feedback.append(f"- Core Technologies: {', '.join(guidance['skills'])}")
        feedback.append(f"- Project Ideas: {guidance['projects']}")
        feedback.append(f"- Focus Areas: {guidance['focus']}")
    else:
        feedback.append("- Research current job postings for your target role")
        feedback.append("- Identify the most frequently mentioned skills and technologies")
        feedback.append("- Build projects that demonstrate practical application")
    
    # Action Plan
    feedback.append("\n**Your Action Plan:**")
    feedback.append("1. 📚 **Learn Missing Skills**: Dedicate 2-3 hours daily to online courses (Coursera, Udemy, freeCodeCamp)")
    
    if missing_skills:
        feedback.append(f"2. 🛠️ **Build Projects**: Create 2-3 portfolio projects showcasing {', '.join(missing_skills[:2])}")
    else:
        feedback.append("2. 🛠️ **Build Projects**: Create portfolio projects that demonstrate your expertise")
    
    feedback.append("3. 📝 **Optimize Resume**: Use action verbs, quantify results, include metrics (e.g., 'Improved performance by 30%')")
    feedback.append("4. 🔗 **Network**: Connect with professionals on LinkedIn, join relevant communities")
    feedback.append("5. 📈 **Track Progress**: Apply to 5-10 jobs weekly, follow up, and refine based on feedback")
    
    return "\n".join(feedback)
