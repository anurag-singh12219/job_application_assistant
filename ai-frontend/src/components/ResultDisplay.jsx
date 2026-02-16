import "./ResultDisplay.css";

export default function ResultDisplay({ result }) {
  if (!result) return null;

  return (
    <div className="results-section">
      <h2>📊 Analysis Results</h2>

      <div className="results-grid">
        <div className="result-card">
          <h3>🎯 Predicted Role</h3>
          <p>{result.predicted_role}</p>
        </div>

        <div className="result-card">
          <h3>⭐ Recommended Role</h3>
          <p>{result.recommended_role}</p>
        </div>

        <div className="result-card ats-score">
          <h3>📈 ATS Score</h3>
          <p>{result.ats_score}%</p>
        </div>

        <div className="result-card salary-card">
          <h3>💰 Salary Estimate</h3>
          <p>${result.salary_estimate_lpa?.toLocaleString() || 0}</p>
        </div>
      </div>

      {result.skills && result.skills.length > 0 && (
        <div className="skills-section">
          <h3>✅ Skills Found in Your Resume</h3>
          <ul className="skills-list">
            {result.skills.map((skill, i) => (
              <li key={i} className="skill-tag">{skill}</li>
            ))}
          </ul>
        </div>
      )}

      {result.missing_skills && result.missing_skills.length > 0 && (
        <div className="missing-skills-section">
          <h3>⚠️ Skills Gap - Recommended to Learn</h3>
          <ul className="skills-list">
            {result.missing_skills.map((skill, i) => (
              <li key={i} className="missing-skill-tag">{skill}</li>
            ))}
          </ul>
        </div>
      )}

      {result.top_job_matches && result.top_job_matches.length > 0 && (
        <div className="job-matches-section">
          <h3>🎯 Top Job Matches</h3>
          <div className="job-matches-list">
            {result.top_job_matches.slice(0, 3).map((job, i) => (
              <div key={i} className="job-match-card">
                <div className="job-match-header">
                  <span className="job-match-role">{job.role}</span>
                  <span className="job-match-score">{job.match_score}% Match</span>
                </div>
                <div className="job-match-salary">Expected: ${job.salary?.toLocaleString()}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="feedback-section">
        <h3>💡 Career Advisor Feedback</h3>
        <p>{result.feedback}</p>
      </div>
    </div>
  );
}

