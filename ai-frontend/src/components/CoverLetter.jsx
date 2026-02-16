import { useState } from "react";
import { generateCoverLetter } from "../api/backend";
import "./CoverLetter.css";

export default function CoverLetter() {
  const [formData, setFormData] = useState({
    userName: "",
    jobTitle: "",
    companyName: "",
    skills: "",
    experienceYears: 0
  });
  const [loading, setLoading] = useState(false);
  const [coverLetter, setCoverLetter] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleGenerate = async () => {
    if (!formData.jobTitle || !formData.companyName) {
      alert("Please fill in at least the job title and company name");
      return;
    }

    setLoading(true);
    try {
      const data = await generateCoverLetter(formData);
      setCoverLetter(data.cover_letter);
    } catch (error) {
      alert("Error generating cover letter. Please try again.");
      console.error(error);
    }
    setLoading(false);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(coverLetter);
    alert("Cover letter copied to clipboard!");
  };

  const handleDownload = () => {
    const blob = new Blob([coverLetter], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `cover-letter-${formData.companyName}.txt`;
    a.click();
  };

  return (
    <div className="cover-letter-page">
      <div className="page-header">
        <h1>✍️ Cover Letter Generator</h1>
        <p>Create professional, AI-powered cover letters in seconds</p>
      </div>

      <div className="cover-letter-grid">
        <div className="form-card">
          <h2>Your Information</h2>

          <div className="form-group">
            <label>Your Name</label>
            <input
              type="text"
              name="userName"
              value={formData.userName}
              onChange={handleChange}
              placeholder="John Doe"
            />
          </div>

          <div className="form-group">
            <label>Job Title *</label>
            <input
              type="text"
              name="jobTitle"
              value={formData.jobTitle}
              onChange={handleChange}
              placeholder="e.g., Software Engineer"
            />
          </div>

          <div className="form-group">
            <label>Company Name *</label>
            <input
              type="text"
              name="companyName"
              value={formData.companyName}
              onChange={handleChange}
              placeholder="e.g., Google"
            />
          </div>

          <div className="form-group">
            <label>Your Key Skills (comma-separated)</label>
            <input
              type="text"
              name="skills"
              value={formData.skills}
              onChange={handleChange}
              placeholder="Python, React, AWS, Machine Learning"
            />
          </div>

          <div className="form-group">
            <label>Years of Experience</label>
            <input
              type="number"
              name="experienceYears"
              value={formData.experienceYears}
              onChange={handleChange}
              min="0"
              max="50"
            />
          </div>

          <button onClick={handleGenerate} disabled={loading} className="generate-btn">
            {loading ? (
              <>
                <span className="spinner"></span>
                Generating...
              </>
            ) : (
              <>
                <span>✨</span>
                Generate Cover Letter
              </>
            )}
          </button>
        </div>

        <div className="preview-card">
          <div className="preview-header">
            <h2>Generated Cover Letter</h2>
            {coverLetter && (
              <div className="preview-actions">
                <button onClick={handleCopy} className="action-btn">
                  📋 Copy
                </button>
                <button onClick={handleDownload} className="action-btn">
                  💾 Download
                </button>
              </div>
            )}
          </div>

          <div className="preview-content">
            {loading ? (
              <div className="loading-state">
                <div className="loading-spinner"></div>
                <p>Crafting your perfect cover letter...</p>
              </div>
            ) : coverLetter ? (
              <pre className="cover-letter-text">{coverLetter}</pre>
            ) : (
              <div className="empty-state">
                <div className="empty-icon">📝</div>
                <p>Your AI-generated cover letter will appear here</p>
                <small>Fill in the form and click Generate</small>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="tips-card">
        <h3>💡 Tips for a Great Cover Letter</h3>
        <ul>
          <li>Customize it for each application - mention specific company achievements</li>
          <li>Keep it concise - aim for 250-300 words</li>
          <li>Show enthusiasm and explain why you're interested in this role</li>
          <li>Highlight your most relevant achievements with quantifiable results</li>
          <li>Proofread carefully before sending</li>
        </ul>
      </div>
    </div>
  );
}
