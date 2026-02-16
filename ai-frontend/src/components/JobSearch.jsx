import { useState } from "react";
import { searchJobs, searchInternships } from "../api/backend";
import "./JobSearch.css";

export default function JobSearch() {
  const [searchData, setSearchData] = useState({
    keywords: "",
    location: "",
    jobType: "",
    experienceLevel: ""
  });
  const [loading, setLoading] = useState(false);
  const [jobs, setJobs] = useState([]);
  const [activeTab, setActiveTab] = useState("jobs");

  const handleChange = (e) => {
    setSearchData({
      ...searchData,
      [e.target.name]: e.target.value
    });
  };

  const handleSearch = async () => {
    if (!searchData.keywords) {
      alert("Please enter keywords");
      return;
    }

    setLoading(true);
    try {
      if (activeTab === "internships") {
        const data = await searchInternships(searchData.keywords, searchData.location || "India");
        setJobs(data.internships || []);
      } else {
        const data = await searchJobs(searchData);
        setJobs(data.jobs || []);
      }
    } catch (error) {
      alert("Error searching jobs. Please try again.");
      console.error(error);
    }
    setLoading(false);
  };

  return (
    <div className="job-search-page">
      <div className="page-header">
        <h1>🎯 Job & Internship Search</h1>
        < p>Find opportunities that match your skills and career goals</p>
      </div>

      <div className="search-tabs">
        <button
          className={`tab-btn ${activeTab === "jobs" ? "active" : ""}`}
          onClick={() => setActiveTab("jobs")}
        >
          💼 Full-time Jobs
        </button>
        <button
          className={`tab-btn ${activeTab === "internships" ? "active" : ""}`}
          onClick={() => setActiveTab("internships")}
        >
          🎓 Internships
        </button>
      </div>

      <div className="search-card">
        <div className="search-form">
          <div className="search-row">
            <div className="search-input-group main">
              <input
                type="text"
                name="keywords"
                value={searchData.keywords}
                onChange={handleChange}
                placeholder="Job title, keywords, or company"
                className="search-input"
              />
            </div>
            <div className="search-input-group">
              <input
                type="text"
                name="location"
                value={searchData.location}
                onChange={handleChange}
                placeholder="Location"
                className="search-input"
              />
            </div>
          </div>

          <div className="filters-row">
            <select name="jobType" value={searchData.jobType} onChange={handleChange} className="filter-select">
              <option value="">All Job Types</option>
              <option value="Full-time">Full-time</option>
              <option value="Part-time">Part-time</option>
              <option value="Contract">Contract</option>
              <option value="Remote">Remote</option>
            </select>

            <select name="experienceLevel" value={searchData.experienceLevel} onChange={handleChange} className="filter-select">
              <option value="">All Experience Levels</option>
              <option value="Entry-level">Entry Level</option>
              <option value="Mid-level">Mid Level</option>
              <option value="Senior">Senior</option>
            </select>

            <button onClick={handleSearch} disabled={loading} className="search-btn">
              {loading ? "Searching..." : "🔍 Search"}
            </button>
          </div>
        </div>
      </div>

      {jobs.length > 0 && (
        <div className="results-section">
          <div className="results-header">
            <h2>{jobs.length} Jobs Found</h2>
          </div>

          <div className="jobs-grid">
            {jobs.map((job, i) => (
              <div key={i} className="job-card">
                <div className="job-header">
                  <div>
                    <h3 className="job-title">{job.title}</h3>
                    <div className="job-company">{job.company}</div>
                  </div>
                  {job.remote && <span className="remote-badge">🌐 Remote</span>}
                </div>

                <div className="job-details">
                  <span className="job-detail">📍 {job.location}</span>
                  <span className="job-detail">💰 {job.salary}</span>
                  <span className="job-detail">⏰ {job.posted}</span>
                </div>

                <p className="job-description">{job.description}</p>

                <div className="job-skills">
                  {job.skills_required?.slice(0, 4).map((skill, idx) => (
                    <span key={idx} className="skill-badge">{skill}</span>
                  ))}
                </div>

                {job.match_score !== undefined && (
                  <div className="match-score">
                    <div className="match-label">Match Score</div>
                    <div className="match-value">{job.match_score}%</div>
                  </div>
                )}

                {job.apply_url ? (
                  <a
                    className="apply-btn"
                    href={job.apply_url}
                    target="_blank"
                    rel="noreferrer"
                  >
                    Apply Now →
                  </a>
                ) : (
                  <button className="apply-btn" disabled>
                    Apply Now →
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {jobs.length === 0 && !loading && searchData.keywords && (
        <div className="no-results">
          <div className="no-results-icon">🔍</div>
          <h3>No jobs found</h3>
          <p>Try adjusting your search criteria or keywords</p>
        </div>
      )}
    </div>
  );
}
