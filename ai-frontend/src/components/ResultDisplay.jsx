import "./ResultDisplay.css";
import { useState } from "react";

export default function ResultDisplay({ result }) {
  const [expandedSection, setExpandedSection] = useState("overview");

  if (!result) return null;

  const toggleSection = (section) => {
    setExpandedSection(expandedSection === section ? null : section);
  };

  return (
    <div className="results-section">
      <div className="results-header">
        <h2>📊 Analysis Results</h2>
        <p className="results-timestamp">Generated just now</p>
      </div>

      <div className="results-grid">
        <div className="result-card primary-card">
          <div className="card-icon">🎯</div>
          <div className="card-content">
            <h3>Predicted Role</h3>
            <p className="card-value">{result.predicted_role}</p>
          </div>
        </div>

        <div className="result-card primary-card">
          <div className="card-icon">⭐</div>
          <div className="card-content">
            <h3>Recommended Role</h3>
            <p className="card-value">{result.recommended_role}</p>
          </div>
        </div>

        <div className="result-card stat-card ats-score">
          <div className="card-icon">📈</div>
          <div className="card-content">
            <h3>ATS Score</h3>
            <div className="score-bar">
              <div 
                className="score-fill" 
                style={{width: `${result.ats_score}%`}}
              ></div>
            </div>
            <p className="card-value">{result.ats_score}%</p>
          </div>
        </div>

        <div className="result-card stat-card salary-card">
          <div className="card-icon">💰</div>
          <div className="card-content">
            <h3>Salary Estimate</h3>
            <p className="card-value">${result.salary_estimate_lpa?.toLocaleString() || 0}</p>
            <p className="card-subtext">LPA</p>
          </div>
        </div>
      </div>

      {result.skills && result.skills.length > 0 && (
        <div className="collapsible-section">
          <div 
            className="section-header"
            onClick={() => toggleSection("skills")}
          >
            <h3>✅ Skills Found in Your Resume</h3>
            <span className="toggle-icon">
              {expandedSection === "skills" ? "▼" : "▶"}
            </span>
          </div>
          {expandedSection === "skills" && (
            <div className="section-content">
              <ul className="skills-list">
                {result.skills.map((skill, i) => (
                  <li key={i} className="skill-tag">{skill}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {result.missing_skills && result.missing_skills.length > 0 && (
        <div className="collapsible-section">
          <div 
            className="section-header warning"
            onClick={() => toggleSection("missing")}
          >
            <h3>⚠️ Skills Gap - Recommended to Learn</h3>
            <span className="toggle-icon">
              {expandedSection === "missing" ? "▼" : "▶"}
            </span>
          </div>
          {expandedSection === "missing" && (
            <div className="section-content">
              <ul className="skills-list">
                {result.missing_skills.map((skill, i) => (
                  <li key={i} className="missing-skill-tag">{skill}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {result.top_job_matches && result.top_job_matches.length > 0 && (
        <div className="collapsible-section">
          <div 
            className="section-header"
            onClick={() => toggleSection("jobs")}
          >
            <h3>🎯 Top Job Matches</h3>
            <span className="toggle-icon">
              {expandedSection === "jobs" ? "▼" : "▶"}
            </span>
          </div>
          {expandedSection === "jobs" && (
            <div className="section-content">
              <div className="job-matches-list">
                {result.top_job_matches.slice(0, 3).map((job, i) => (
                  <div key={i} className="job-match-card">
                    <div className="job-match-header">
                      <span className="job-match-role">{job.role}</span>
                      <span className={`job-match-score ${
                        job.match_score >= 80 ? 'excellent' : 
                        job.match_score >= 60 ? 'good' : 'fair'
                      }`}>
                        {job.match_score}% Match
                      </span>
                    </div>
                    <div className="job-match-salary">
                      💼 Expected: ${job.salary?.toLocaleString()}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      <div className="feedback-section">
        <div className="feedback-header">
          <h3>💡 Career Advisor Feedback</h3>
        </div>
        <div className="feedback-content">
          <p>{result.feedback}</p>
        </div>
      </div>

      <div className="action-buttons">
        <button className="btn-primary">📥 Download Report</button>
        <button className="btn-secondary">🔄 New Analysis</button>
      </div>
    </div>
  );
}

