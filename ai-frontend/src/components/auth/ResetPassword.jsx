import { useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { authAPI } from "../../api/backend";
import FormInput from "./FormInput";
import PasswordStrengthMeter from "./PasswordStrengthMeter";
import "./Auth.css";

export default function ResetPassword() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token") || "";
  const navigate = useNavigate();

  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage("");
    setSuccessMessage("");

    if (!token) {
      setErrorMessage("Missing or invalid password reset token.");
      return;
    }
    if (password.length < 8) {
      setErrorMessage("Password must be at least 8 characters long.");
      return;
    }
    if (password !== confirmPassword) {
      setErrorMessage("Passwords do not match.");
      return;
    }

    setLoading(true);
    try {
      const data = await authAPI.resetPassword({
        token,
        password,
        confirm_password: confirmPassword
      });
      setSuccessMessage(data.message || "Password reset successful! Redirecting to login...");
      setTimeout(() => {
        navigate("/login");
      }, 2500);
    } catch (err) {
      const detail = err.response?.data?.detail;
      setErrorMessage(detail || "Failed to reset password. The link may have expired or been used.");
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
              <path d="M21 2l-2 2m-2-2l2 2" />
              <path d="M15.5 8.5l1.5 1.5" />
              <path d="M12 12l6-6a3 3 0 0 0-4.24-4.24l-6 6a6 6 0 1 0 8.48 8.48l1.76-1.76" />
            </svg>
          </div>
          <h1 className="auth-title">Choose New Password</h1>
          <p className="auth-subtitle">Create a secure password for your account</p>
        </div>

        {!token && (
          <div className="auth-alert auth-alert-error" role="alert">
            <span className="auth-alert-icon">⚠️</span>
            <span>No reset token provided in the link. Please request a new password reset.</span>
          </div>
        )}

        {errorMessage && (
          <div className="auth-alert auth-alert-error" role="alert">
            <span className="auth-alert-icon">⚠️</span>
            <span>{errorMessage}</span>
          </div>
        )}

        {successMessage && (
          <div className="auth-alert auth-alert-success" role="alert">
            <span className="auth-alert-icon">✓</span>
            <span>{successMessage}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} noValidate>
          <FormInput
            id="reset-new-password"
            label="New Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
            required
            autoComplete="new-password"
            disabled={loading || !token}
          />

          <PasswordStrengthMeter password={password} />

          <FormInput
            id="reset-confirm-password"
            label="Confirm New Password"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            placeholder="••••••••"
            required
            autoComplete="new-password"
            disabled={loading || !token}
          />

          <button
            type="submit"
            className="auth-submit-btn"
            disabled={loading || !token || !password}
          >
            {loading ? (
              <>
                <span className="auth-spinner" />
                <span>Updating Password...</span>
              </>
            ) : (
              <span>Save & Sign In</span>
            )}
          </button>
        </form>

        <div className="auth-footer">
          <Link to="/login">Back to Login</Link>
        </div>
      </div>
    </div>
  );
}
