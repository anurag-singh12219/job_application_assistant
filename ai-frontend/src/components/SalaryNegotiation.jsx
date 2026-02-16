import { useState } from "react";
import { getSalaryInsights } from "../api/backend";
import "./SalaryNegotiation.css";

export default function SalaryNegotiation() {
  const [formData, setFormData] = useState({
    jobTitle: "",
    location: "",
    experienceYears: 0,
    skills: ""
  });
  const [loading, setLoading] = useState(false);
  const [insights, setInsights] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleGetInsights = async () => {
    if (!formData.jobTitle) {
      alert("Please fill in the job title");
      return;
    }

    setLoading(true);
    try {
      const skillsList = formData.skills.split(",").map(s => s.trim()).filter(s => s);
      const data = await getSalaryInsights({
        job_title: formData.jobTitle,
        location: formData.location || "United States",
        experience_years: parseInt(formData.experienceYears),
        skills: skillsList
      });
      setInsights(data);
    } catch (error) {
      alert("Error getting salary insights. Please try again.");
      console.error(error);
    }
    setLoading(false);
  };

  const formatSalary = (amount, currency = "USD") => {
    if (currency === "INR") {
      return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }).format(amount);
    }
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  };

  return (
    <div className="salary-page">
      <div className="page-header">
        <h1>💰 Salary Negotiation</h1>
        <p>Get market insights and negotiation strategies powered by AI</p>
      </div>

      <div className="salary-form-card">
        <h2>Your Profile</h2>
        <div className="form-row">
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
            <label>Location</label>
            <select
              name="location"
              value={formData.location}
              onChange={handleChange}
              style={{width: '100%', padding: '12px', border: '1px solid #e2e8f0', borderRadius: '8px', fontSize: '14px'}}
            >
              <option value="">Select or type a location</option>
              <optgroup label="United States">
                <option value="San Francisco, CA">San Francisco, CA</option>
                <option value="New York, NY">New York, NY</option>
                <option value="Los Angeles, CA">Los Angeles, CA</option>
                <option value="Seattle, WA">Seattle, WA</option>
                <option value="Austin, TX">Austin, TX</option>
                <option value="Boston, MA">Boston, MA</option>
                <option value="Remote, USA">Remote, USA</option>
              </optgroup>
              <optgroup label="India">
                <option value="Bangalore, India">Bangalore, India</option>
                <option value="Mumbai, India">Mumbai, India</option>
                <option value="Delhi, India">Delhi, India</option>
                <option value="Hyderabad, India">Hyderabad, India</option>
                <option value="Pune, India">Pune, India</option>
                <option value="Chennai, India">Chennai, India</option>
                <option value="Remote, India">Remote, India</option>
              </optgroup>
              <optgroup label="Other">
                <option value="London, UK">London, UK</option>
                <option value="Toronto, Canada">Toronto, Canada</option>
              </optgroup>
            </select>
          </div>
        </div>

        <div className="form-row">
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

          <div className="form-group">
            <label>Key Skills</label>
            <input
              type="text"
              name="skills"
              value={formData.skills}
              onChange={handleChange}
              placeholder="Python, AWS, Docker"
            />
          </div>
        </div>

        <button onClick={handleGetInsights} disabled={loading} className="insights-btn">
          {loading ? (
            <>
              <span className="spinner"></span>
              Analyzing Market Data...
            </>
          ) : (
            <>
              <span>📊</span>
              Get Salary Insights
            </>
          )}
        </button>
      </div>

      {insights && (
        <div className="insights-results">
          <div className="salary-range-card">
            <h2>💵 Estimated Salary Range</h2>
            <div className="salary-range">
              <div className="salary-item">
                <div className="salary-label">Minimum</div>
                <div className="salary-value">{formatSalary(insights.estimated_salary_range.min, insights.estimated_salary_range.currency)}</div>
              </div>
              <div className="salary-item target">
                <div className="salary-label">Target</div>
                <div className="salary-value">{formatSalary(insights.estimated_salary_range.target, insights.estimated_salary_range.currency)}</div>
              </div>
              <div className="salary-item">
                <div className="salary-label">Maximum</div>
                <div className="salary-value">{formatSalary(insights.estimated_salary_range.max, insights.estimated_salary_range.currency)}</div>
              </div>
            </div>
            <div className="salary-note">
              <small>Based on {formData.experienceYears} years of experience in {formData.location || "United States"}</small>
            </div>
          </div>

          <div className="advice-card">
            <h2>🎯 Negotiation Strategy</h2>
            <div className="advice-content">
              {insights.negotiation_advice.split('\n').map((line, i) => (
                line.trim() && <p key={i}>{line}</p>
              ))}
            </div>
          </div>

          <div className="factors-card">
            <h3>📈 Key Factors Affecting Your Salary</h3>
            <ul className="factors-list">
              {insights.key_factors?.map((factor, i) => (
                <li key={i}>{factor}</li>
              ))}
            </ul>
          </div>
        </div>
      )}

      <div className="tips-grid">
        <div className="tip-card">
          <div className="tip-icon">🎯</div>
          <h3>Do Your Research</h3>
          <p>Know the market rate for your role and location. Use multiple sources like Glassdoor, LinkedIn, and Payscale.</p>
        </div>

        <div className="tip-card">
          <div className="tip-icon">⏰</div>
          <h3>Timing Matters</h3>
          <p>Wait for the official offer before discussing salary. Don't bring it up in the first interview.</p>
        </div>

        <div className="tip-card">
          <div className="tip-icon">💪</div>
          <h3>Be Confident</h3>
          <p>Know your value and be prepared to articulate it with specific examples of your achievements.</p>
        </div>

        <div className="tip-card">
          <div className="tip-icon">🤝</div>
          <h3>Stay Professional</h3>
          <p>Use collaborative language. Frame it as "finding a number that works for both of us."</p>
        </div>
      </div>
    </div>
  );
}
