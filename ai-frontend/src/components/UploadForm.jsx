import { useState } from "react";
import { analyzeResume } from "../api/backend";

export default function UploadForm({ setResult }) {
  const [file, setFile] = useState(null);
  const [jobDesc, setJobDesc] = useState("");
  const [loading, setLoading] = useState(false);
  const [fileName, setFileName] = useState("");

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setFileName(selectedFile.name);
    }
  };

  const handleSubmit = async () => {
    if (!file) {
      alert("Please upload your resume first!");
      return;
    }

    if (!jobDesc.trim()) {
      alert("Please paste the job description!");
      return;
    }

    setLoading(true);

    try {
      const data = await analyzeResume(file, jobDesc);
      setResult(data);
    } catch (error) {
      alert("Error: Backend server is not running or there was a problem processing your request.");
      console.error(error);
    }

    setLoading(false);
  };

  return (
    <div className="upload-section">
      <h2>📄 Upload Your Resume</h2>

      <div className="file-input-wrapper">
        <label htmlFor="resume-upload">Resume (PDF only)</label>
        <input 
          id="resume-upload"
          type="file" 
          accept=".pdf"
          onChange={handleFileChange}
        />
        {fileName && <p style={{marginTop: '8px', color: '#667eea', fontSize: '14px'}}>✓ {fileName}</p>}
      </div>

      <div className="textarea-wrapper">
        <label htmlFor="job-description">Job Description</label>
        <textarea
          id="job-description"
          placeholder="Paste the job description here... Include required skills, responsibilities, and qualifications."
          rows="8"
          value={jobDesc}
          onChange={(e) => setJobDesc(e.target.value)}
        />
      </div>

      <button onClick={handleSubmit} disabled={loading}>
        {loading ? (
          <>
            <span className="loading"></span>
            Analyzing Your Resume...
          </>
        ) : (
          "🚀 Analyze Resume"
        )}
      </button>
    </div>
  );
}
