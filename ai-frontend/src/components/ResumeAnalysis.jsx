import { useState, useRef } from "react";
import { analyzeResume } from "../api/backend";
import "./ResumeAnalysis.css";

export default function ResumeAnalysis() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState("");
  const fileInputRef = useRef(null);

  const handleFileSelect = (e) => {
    const file = e.target.files?.[0];
    if (file && file.type === "application/pdf") {
      setResumeFile(file);
      setError("");
    } else {
      setError("Please select a valid PDF file");
      setResumeFile(null);
    }
  };

  const handleAnalyze = async () => {
    if (!resumeFile || !jobDescription.trim()) {
      setError("Please upload a resume PDF and enter a job description");
      return;
    }

    setLoading(true);
    setError("");
    try {
      const formData = new FormData();
      formData.append("file", resumeFile);
      formData.append("job_description", jobDescription);

      const result = await analyzeResume(formData);
      setAnalysis(result);
    } catch (err) {
      setError(err.message || "Analysis failed. Please try again.");
      console.error(err);
    }
    setLoading(false);
  };

  const handleReset = () => {
    setResumeFile(null);
    setJobDescription("");
    setAnalysis(null);
    setError("");
    fileInputRef.current.value = "";
  };

  if (analysis) {
    return (
      <div className="resume-analysis-page">
        <div className="page-header">
          <h1>📊 Resume Analysis Complete</h1>
          <button className="btn-reset" onClick={handleReset}>← Start New Analysis</button>
        </div>

        <div className="analysis-container">
          {/* Summary Cards */}
          <div className="summary-grid">
            <div className="summary-card score-high">
              <div className="ats-score-display">
                <div className="score-percentile">{Math.round(analysis.ats_score)}/100</div>
              </div>
              <div className="card-label">ATS Compatibility Score</div>
              <div className="card-status">
                {analysis.ats_score >= 80 ? "✅ Excellent" : analysis.ats_score >= 60 ? "⚡ Good" : "⚠️ Needs Work"}
              </div>
            </div>

            <div className="summary-card">
              <div className="card-value">{analysis.skills?.length || 0}</div>
              <div className="card-label">Skills Identified</div>
              <div className="card-status">Technical competencies</div>
            </div>

            <div className="summary-card">
              <div className="card-value">{analysis.missing_skills?.length || 0}</div>
              <div className="card-label">Skills to Develop</div>
              <div className="card-status">Growth opportunities</div>
            </div>

            <div className="summary-card">
              <div className="card-value">${analysis.salary_estimate_lpa}L</div>
              <div className="card-label">Salary Range</div>
              <div className="card-status">Market estimate</div>
            </div>
          </div>

          {/* Detailed Feedback */}
          <div className="details-section">
            <h2>🎯 AI-Powered Feedback & Recommendations</h2>
            <div className="feedback-box">
              {analysis.feedback ? (
                <div className="feedback-content">
                  {analysis.feedback.split('\n').map((line, idx) => (
                    line.trim() && <p key={idx}>{line}</p>
                  ))}
                </div>
              ) : (
                <p>No feedback available</p>
              )}
            </div>
          </div>

          {/* Skills Section */}
          <div className="details-section">
            <h2>✨ Your Technical Skills ({analysis.skills?.length})</h2>
            <div className="skills-container">
              {analysis.skills && analysis.skills.length > 0 ? (
                analysis.skills.map((skill, idx) => (
                  <span key={idx} className="skill-badge">{skill}</span>
                ))
              ) : (
                <p className="no-data">No skills detected in resume</p>
              )}
            </div>
          </div>

          {/* Missing Skills */}
          {analysis.missing_skills && analysis.missing_skills.length > 0 && (
            <div className="details-section">
              <h2>📚 Skills to Develop</h2>
              <div className="missing-skills-container">
                {analysis.missing_skills.map((skill, idx) => (
                  <div key={idx} className="missing-skill-item">
                    <span className="skill-name">{skill}</span>
                    <span className="skill-priority">Priority</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Job Matches */}
          {analysis.top_job_matches && analysis.top_job_matches.length > 0 && (
            <div className="details-section">
              <h2>🎯 Top Job Matches for Your Profile</h2>
              <div className="job-matches">
                {analysis.top_job_matches.map((job, idx) => (
                  <div key={idx} className="job-match-card">
                    <div className="job-header">
                      <h3>{job.role}</h3>
                      <span className="match-score">{Math.round(job.match_score)}% fit</span>
                    </div>
                    <div className="job-salary">💰 ₹{job.salary}L LPA</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="resume-analysis-page">
      <div className="page-header">
        <h1>📄 Resume Analysis</h1>
        <p>Upload your resume and get instant AI-powered feedback with ATS score, skill analysis, and personalized recommendations</p>
      </div>

      <div className="analysis-form-container">
        <div className="form-card">
          <h2>Step 1: Upload Your Resume</h2>
          
          <div className="file-upload-area">
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf"
              onChange={handleFileSelect}
              className="file-input"
              id="resume-file"
            />
            <label htmlFor="resume-file" className="file-label">
              <div className="upload-icon">📎</div>
              <p className="upload-text">
                {resumeFile ? `✓ ${resumeFile.name}` : "Click to upload PDF resume"}
              </p>
              <p className="upload-hint">PDF format, max 10MB</p>
            </label>
          </div>

          <h2 style={{ marginTop: "30px" }}>Step 2: Job Description</h2>
          <div className="form-group">
            <label>Paste the job description you're targeting:</label>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste the complete job description here for better analysis..."
              className="job-description-input"
            />
          </div>

          {error && <div className="error-message">❌ {error}</div>}

          <button 
            onClick={handleAnalyze}
            disabled={loading || !resumeFile || !jobDescription.trim()}
            className="btn-analyze"
          >
            {loading ? "🔄 Analyzing..." : "🚀 Analyze Resume"}
          </button>

          <div className="info-box">
            <p>💡 <strong>Tip:</strong> The more detailed your job description, the more accurate our AI analysis will be.</p>
          </div>
        </div>

        <div className="info-card">
          <h3>What You'll Get:</h3>
          <ul>
            <li>📊 ATS Compatibility Score</li>
            <li>✨ Extracted Technical Skills</li>
            <li>🎯 Role Prediction & Recommendations</li>
            <li>📚 Missing Skills Analysis</li>
            <li>💼 Salary Estimates</li>
            <li>🤖 AI-Powered Personalized Feedback</li>
            <li>🌟 Actionable Improvement Tips</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
