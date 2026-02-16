import { useState } from "react";
import { getInterviewPrep } from "../api/backend";
import "./InterviewPrep.css";

export default function InterviewPrep() {
  const [formData, setFormData] = useState({
    jobTitle: "",
    companyName: "",
    jobDescription: "",
    skills: ""
  });
  const [loading, setLoading] = useState(false);
  const [prepData, setPrepData] = useState(null);
  const [expandedQuestion, setExpandedQuestion] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleGenerate = async () => {
    if (!formData.jobTitle) {
      alert("Please fill in the job title");
      return;
    }

    setLoading(true);
    try {
      const skillsList = formData.skills.split(",").map(s => s.trim()).filter(s => s);
      const data = await getInterviewPrep({
        job_title: formData.jobTitle,
        company_name: formData.companyName,
        job_description: formData.jobDescription,
        skills: skillsList
      });
      setPrepData(data);
    } catch (error) {
      alert("Error generating interview prep. Please try again.");
      console.error(error);
    }
    setLoading(false);
  };

  return (
    <div className="interview-prep-page">
      <div className="page-header">
        <h1>💬 Interview Preparation</h1>
        <p>Get AI-generated interview questions and preparation strategies</p>
      </div>

      <div className="prep-form-card">
        <h2>Job Details</h2>
        <div className="form-row">
          <div className="form-group">
            <label>Job Title *</label>
            <input
              type="text"
              name="jobTitle"
              value={formData.jobTitle}
              onChange={handleChange}
              placeholder="e.g., Senior Data Scientist"
            />
          </div>

          <div className="form-group">
            <label>Company Name</label>
            <input
              type="text"
              name="companyName"
              value={formData.companyName}
              onChange={handleChange}
              placeholder="e.g., Microsoft"
            />
          </div>
        </div>

        <div className="form-group">
          <label>Key Skills (comma-separated)</label>
          <input
            type="text"
            name="skills"
            value={formData.skills}
            onChange={handleChange}
            placeholder="Python, Machine Learning, SQL, AWS"
          />
        </div>

        <div className="form-group">
          <label>Job Description (Optional)</label>
          <textarea
            name="jobDescription"
            value={formData.jobDescription}
            onChange={handleChange}
            rows="4"
            placeholder="Paste the job description for more tailored questions..."
          />
        </div>

        <button onClick={handleGenerate} disabled={loading} className="prep-btn">
          {loading ? (
            <>
              <span className="spinner"></span>
              Generating Interview Questions...
            </>
          ) : (
            <>
              <span>🎯</span>
              Generate Interview Prep
            </>
          )}
        </button>
      </div>

      {prepData && (
        <div className="prep-results">
          <div className="questions-section">
            <h2>📝 Technical Questions</h2>
            <div className="questions-list">
              {(prepData.questions?.technical_questions && prepData.questions.technical_questions.length > 0) ? (
                prepData.questions.technical_questions.map((q, i) => (
                  <div key={i} className="question-card" onClick={() => setExpandedQuestion(expandedQuestion === `tech-${i}` ? null : `tech-${i}`)}>
                    <div className="question-header">
                      <div className="question-number">Q{i + 1}</div>
                      <div className="question-text">{q.length > 100 ? q.substring(0, 100) + "..." : q}</div>
                      <span className={`expand-icon ${expandedQuestion === `tech-${i}` ? 'expanded' : ''}`}>▼</span>
                    </div>
                    {expandedQuestion === `tech-${i}` && (
                      <div className="question-full">{q}</div>
                    )}
                  </div>
                ))
              ) : (
                <div className="no-questions">
                  <p>🤔 No technical questions generated. Try again with more specific job details.</p>
                </div>
              )}
            </div>
          </div>

          <div className="questions-section">
            <h2>🎭 Behavioral Questions</h2>
            <div className="questions-list">
              {(prepData.questions?.behavioral_questions && prepData.questions.behavioral_questions.length > 0) ? (
                prepData.questions.behavioral_questions.map((q, i) => (
                  <div key={i} className="question-card" onClick={() => setExpandedQuestion(expandedQuestion === `behav-${i}` ? null : `behav-${i}`)}>
                    <div className="question-header">
                      <div className="question-number">Q{i + 1}</div>
                      <div className="question-text">{q.length > 100 ? q.substring(0, 100) + "..." : q}</div>
                      <span className={`expand-icon ${expandedQuestion === `behav-${i}` ? 'expanded' : ''}`}>▼</span>
                    </div>
                    {expandedQuestion === `behav-${i}` && (
                      <div className="question-full">{q}</div>
                    )}
                  </div>
                ))
              ) : (
                <div className="no-questions">
                  <p>🤔 No behavioral questions generated. Try again with more specific job details.</p>
                </div>
              )}
            </div>
          </div>

          <div className="questions-section">
            <h2>❓ Questions to Ask the Interviewer</h2>
            <div className="questions-list">
              {(prepData.questions?.questions_to_ask && prepData.questions.questions_to_ask.length > 0) ? (
                prepData.questions.questions_to_ask.map((q, i) => (
                  <div key={i} className="question-card" onClick={() => setExpandedQuestion(expandedQuestion === `ask-${i}` ? null : `ask-${i}`)}>
                    <div className="question-header">
                      <div className="question-number">{i + 1}</div>
                      <div className="question-text">{q.length > 100 ? q.substring(0, 100) + "..." : q}</div>
                      <span className={`expand-icon ${expandedQuestion === `ask-${i}` ? 'expanded' : ''}`}>▼</span>
                    </div>
                    {expandedQuestion === `ask-${i}` && (
                      <div className="question-full">{q}</div>
                    )}
                  </div>
                ))
              ) : (
                <div className="no-questions">
                  <p>💭 No counter-questions generated. Try again with more specific job details.</p>
                </div>
              )}
            </div>
          </div>

          {prepData.preparation_tips && (
            <div className="tips-section">
              <h2>💡 Preparation Tips</h2>
              <div className="tips-content">
                {prepData.preparation_tips.split('\n').map((line, i) => (
                  line.trim() && <p key={i}>{line}</p>
                ))}
              </div>
            </div>
          )}

          {prepData.general_advice && prepData.general_advice.length > 0 && (
            <div className="advice-section">
              <h3>🎯 General Interview Advice</h3>
              <ul>
                {prepData.general_advice.map((tip, i) => (
                  <li key={i}>{tip}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
