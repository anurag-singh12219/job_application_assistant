import { useState } from "react";
import { analyzeResume } from "../api/backend";
import "./UploadForm.css";

export default function UploadForm({ setResult }) {
  const [file, setFile] = useState(null);
  const [jobDesc, setJobDesc] = useState("");
  const [loading, setLoading] = useState(false);
  const [fileName, setFileName] = useState("");
  const [error, setError] = useState("");
  const [dragActive, setDragActive] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    handleFile(selectedFile);
  };

  const handleFile = (selectedFile) => {
    setError("");
    if (!selectedFile) return;

    // Validate file type
    if (selectedFile.type !== "application/pdf" && !selectedFile.name.endsWith(".pdf")) {
      setError("Only PDF files are supported. Please upload a PDF resume.");
      return;
    }

    // Validate file size (max 5MB)
    if (selectedFile.size > 5 * 1024 * 1024) {
      setError("File size exceeds 5MB. Please upload a smaller file.");
      return;
    }

    setFile(selectedFile);
    setFileName(selectedFile.name);
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleSubmit = async () => {
    setError("");

    if (!file) {
      setError("Please upload your resume first!");
      return;
    }

    if (!jobDesc.trim()) {
      setError("Please paste the job description!");
      return;
    }

    if (jobDesc.trim().length < 50) {
      setError("Job description should be at least 50 characters long.");
      return;
    }

    setLoading(true);

    try {
      const data = await analyzeResume(file, jobDesc);
      setResult(data);
      // Reset form after successful analysis
      setFile(null);
      setFileName("");
      setJobDesc("");
    } catch (error) {
      setError("Error: Backend server is not running or there was a problem processing your request.");
      console.error(error);
    }

    setLoading(false);
  };

  const clearForm = () => {
    setFile(null);
    setFileName("");
    setJobDesc("");
    setError("");
  };

  return (
    <div className="upload-section">
      <div className="upload-header">
        <h2>📄 Analyze Your Resume</h2>
        <p className="upload-subtitle">Get AI-powered insights to match your skills with job requirements</p>
      </div>

      {error && (
        <div className="error-message">
          <span className="error-icon">⚠️</span>
          <span>{error}</span>
        </div>
      )}

      <div className="upload-container">
        <div className="upload-left">
          <div 
            className={`file-upload-area ${dragActive ? "active" : ""} ${fileName ? "has-file" : ""}`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <label htmlFor="resume-upload" className="file-label">
              <div className="upload-icon">📥</div>
              <div className="upload-text">
                <span className="upload-title">Upload Your Resume</span>
                <span className="upload-description">PDF format, max 5MB</span>
              </div>
              <input 
                id="resume-upload"
                type="file" 
                accept=".pdf"
                onChange={handleFileChange}
              />
            </label>
            {fileName && (
              <div className="file-preview">
                <span className="file-icon">✓</span>
                <span className="file-name">{fileName}</span>
              </div>
            )}
          </div>

          <div className="form-tips">
            <h4>📋 Tips for Better Analysis:</h4>
            <ul>
              <li>Use a clear, ATS-friendly resume format</li>
              <li>Include all relevant skills and experiences</li>
              <li>Ensure contact information is up to date</li>
              <li>Paste the complete job description</li>
            </ul>
          </div>
        </div>

        <div className="upload-right">
          <div className="textarea-wrapper">
            <label htmlFor="job-description">Job Description</label>
            <textarea
              id="job-description"
              placeholder="Paste the job description here...&#10;Include:&#10;• Required skills&#10;• Responsibilities&#10;• Qualifications&#10;• Experience level"
              rows="10"
              value={jobDesc}
              onChange={(e) => setJobDesc(e.target.value)}
            />
            <div className="textarea-counter">
              {jobDesc.length} characters
            </div>
          </div>
        </div>
      </div>

      <div className="form-actions">
        <button 
          className="btn-analyze" 
          onClick={handleSubmit} 
          disabled={loading || !file}
        >
          {loading ? (
            <>
              <span className="loading-spinner"></span>
              <span>Analyzing Your Resume...</span>
            </>
          ) : (
            <>
              <span>🚀</span>
              <span>Analyze Resume</span>
            </>
          )}
        </button>

        <button 
          className="btn-clear" 
          onClick={clearForm}
          disabled={loading}
        >
          Clear
        </button>
      </div>

      <div className="analysis-info">
        <p>✨ Our AI model analyzes your resume against the job description to provide personalized insights and recommendations.</p>
      </div>
    </div>
  );
}

