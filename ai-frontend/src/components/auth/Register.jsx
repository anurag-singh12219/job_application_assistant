import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import FormInput from "./FormInput";
import PasswordStrengthMeter from "./PasswordStrengthMeter";
import "./Auth.css";

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [acceptTerms, setAcceptTerms] = useState(false);

  const [fieldErrors, setFieldErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const validate = () => {
    const errors = {};
    if (!fullName.trim() || fullName.trim().length < 2) {
      errors.fullName = "Please enter your full name (at least 2 characters).";
    }
    if (!email.trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      errors.email = "Please enter a valid email address.";
    }
    if (password.length < 8) {
      errors.password = "Password must be at least 8 characters.";
    }
    if (password !== confirmPassword) {
      errors.confirmPassword = "Passwords do not match.";
    }
    if (!acceptTerms) {
      errors.acceptTerms = "You must accept the terms of service and privacy policy.";
    }
    setFieldErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage("");
    setSuccessMessage("");

    if (!validate()) {
      return;
    }

    setLoading(true);
    try {
      const data = await register({
        full_name: fullName,
        email: email,
        password: password,
        confirm_password: confirmPassword,
        accept_terms: acceptTerms
      });
      setSuccessMessage(data.message || "Registration successful! Please check your email to verify your account.");
      setTimeout(() => {
        navigate("/login");
      }, 3000);
    } catch (err) {
      const detail = err.response?.data?.detail;
      setErrorMessage(detail || "Registration failed. Please verify your details.");
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
              <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
              <circle cx="8.5" cy="7" r="4" />
              <line x1="20" y1="8" x2="20" y2="14" />
              <line x1="23" y1="11" x2="17" y2="11" />
            </svg>
          </div>
          <h1 className="auth-title">Create Account</h1>
          <p className="auth-subtitle">Join thousands accelerating their career with JobPilot AI</p>
        </div>

        {errorMessage && (
          <div className="auth-alert auth-alert-error" role="alert">
            <span className="auth-alert-icon">⚠️</span>
            <span>{errorMessage}</span>
          </div>
        )}

        {successMessage && (
          <div className="auth-alert auth-alert-success" role="alert">
            <span className="auth-alert-icon">✓</span>
            <span>{successMessage} Redirecting to login...</span>
          </div>
        )}

        <form onSubmit={handleSubmit} noValidate>
          <FormInput
            id="register-name"
            label="Full Name"
            type="text"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            placeholder="Jane Doe"
            required
            autoComplete="name"
            error={fieldErrors.fullName}
            disabled={loading}
          />

          <FormInput
            id="register-email"
            label="Email Address"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="jane@example.com"
            required
            autoComplete="email"
            error={fieldErrors.email}
            disabled={loading}
          />

          <FormInput
            id="register-password"
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
            required
            autoComplete="new-password"
            error={fieldErrors.password}
            disabled={loading}
          />

          <PasswordStrengthMeter password={password} />

          <FormInput
            id="register-confirm-password"
            label="Confirm Password"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            placeholder="••••••••"
            required
            autoComplete="new-password"
            error={fieldErrors.confirmPassword}
            disabled={loading}
          />

          <div className="auth-form-group">
            <label className="auth-checkbox-label">
              <input
                type="checkbox"
                className="auth-checkbox"
                checked={acceptTerms}
                onChange={(e) => setAcceptTerms(e.target.checked)}
                disabled={loading}
              />
              <span>I agree to the Terms of Service & Privacy Policy</span>
            </label>
            {fieldErrors.acceptTerms && (
              <p className="auth-input-error">{fieldErrors.acceptTerms}</p>
            )}
          </div>

          <button
            type="submit"
            className="auth-submit-btn"
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="auth-spinner" />
                <span>Creating Account...</span>
              </>
            ) : (
              <span>Create Account</span>
            )}
          </button>
        </form>

        <div className="auth-footer">
          Already have an account?
          <Link to="/login">Sign in here</Link>
        </div>
      </div>
    </div>
  );
}
