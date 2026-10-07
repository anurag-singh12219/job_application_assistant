import { Link } from "react-router-dom";
import "./Auth.css";

export default function Unauthorized() {
  return (
    <div className="auth-page-container">
      <div className="auth-card" style={{ textAlign: "center" }}>
        <div className="auth-header">
          <div className="auth-logo-badge" style={{ borderColor: "rgba(239, 68, 68, 0.4)", color: "#ef4444" }}>
            <svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10" />
              <line x1="4.93" y1="4.93" x2="19.07" y2="19.07" />
            </svg>
          </div>
          <h1 className="auth-title">403 - Access Forbidden</h1>
          <p className="auth-subtitle">
            You do not possess the required administrator privileges to access this area.
          </p>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: "12px", marginTop: "20px" }}>
          <Link to="/" className="btn-brand-solid" style={{ justifyContent: "center" }}>
            Return to Homepage
          </Link>
          <Link to="/profile" className="btn-secondary-outline" style={{ justifyContent: "center" }}>
            View Your Profile
          </Link>
        </div>
      </div>
    </div>
  );
}
