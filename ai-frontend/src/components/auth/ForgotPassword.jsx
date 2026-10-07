import { useState } from "react";
import { Link } from "react-router-dom";
import { authAPI } from "../../api/backend";
import FormInput from "./FormInput";
import "./Auth.css";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email.trim()) return;

    setLoading(true);
    try {
      const data = await authAPI.forgotPassword(email);
      setMessage(data.message || "If an account with that email exists, password reset instructions have been sent.");
      setSubmitted(true);
    } catch {
      // Always show generic success message to prevent email enumeration
      setMessage("If an account with that email exists, password reset instructions have been sent.");
      setSubmitted(true);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page-container">
      <div className="auth-card">
        <div className="auth-header">
          <div className="auth-logo-badge">
            <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
              <path d="M7 11V7a5 5 0 0 1 10 0v4" />
            </svg>
          </div>
          <h1 className="auth-title">Reset Password</h1>
          <p className="auth-subtitle">
            Enter your account email to receive secure recovery instructions
          </p>
        </div>

        {submitted ? (
          <div>
            <div className="auth-alert auth-alert-success" role="alert">
              <span className="auth-alert-icon">✓</span>
              <span>{message}</span>
            </div>
            <p className="auth-input-helper" style={{ textAlign: "center", marginBottom: "20px" }}>
              Please check your inbox (and spam folder) for the password reset link.
            </p>
            <Link to="/login" className="btn-brand-solid" style={{ width: "100%", justifyContent: "center" }}>
              Return to Login
            </Link>
          </div>
        ) : (
          <form onSubmit={handleSubmit} noValidate>
            <FormInput
              id="forgot-email"
              label="Account Email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="name@company.com"
              required
              autoComplete="email"
              disabled={loading}
              helperText="We'll never disclose whether this email exists in our system."
            />

            <button
              type="submit"
              className="auth-submit-btn"
              disabled={loading || !email}
            >
              {loading ? (
                <>
                  <span className="auth-spinner" />
                  <span>Sending Instructions...</span>
                </>
              ) : (
                <span>Send Reset Link</span>
              )}
            </button>
          </form>
        )}

        <div className="auth-footer">
          Remember your password?
          <Link to="/login">Back to Sign In</Link>
        </div>
      </div>
    </div>
  );
}
