import { useState, useEffect, useCallback } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { authAPI } from "../../api/backend";
import { useAuth } from "../../context/AuthContext";
import FormInput from "./FormInput";
import "./Auth.css";

export default function VerifyEmail() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token") || "";
  const { refreshUser } = useAuth();

  const [statusState, setStatusState] = useState("idle"); // idle, verifying, success, error
  const [statusMessage, setStatusMessage] = useState("");

  const [resendEmail, setResendEmail] = useState("");
  const [resending, setResending] = useState(false);
  const [resendMessage, setResendMessage] = useState("");

  const handleVerify = useCallback(async (tokenToVerify) => {
    setStatusState("verifying");
    setStatusMessage("");

    try {
      const data = await authAPI.verifyEmail(tokenToVerify);
      setStatusState("success");
      setStatusMessage(data.message || "Email verified successfully!");
      refreshUser();
    } catch (err) {
      setStatusState("error");
      const detail = err.response?.data?.detail;
      setStatusMessage(detail || "Invalid or expired verification link.");
    }
  }, [refreshUser]);

  useEffect(() => {
    if (token) {
      handleVerify(token);
    }
  }, [token, handleVerify]);

  const handleResend = async (e) => {
    e.preventDefault();
    if (!resendEmail.trim()) return;

    setResending(true);
    setResendMessage("");
    try {
      const data = await authAPI.resendVerification(resendEmail);
      setResendMessage(data.message || "If this account is unverified, a new link has been sent.");
    } catch {
      setResendMessage("If this account is unverified, a new link has been sent.");
    } finally {
      setResending(false);
    }
  };

  return (
    <div className="auth-page-container">
      <div className="auth-card">
        <div className="auth-header">
          <div className="auth-logo-badge">
            <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
              <polyline points="22,6 12,13 2,6" />
            </svg>
          </div>
          <h1 className="auth-title">Email Verification</h1>
          <p className="auth-subtitle">Confirm your email address to unlock all features</p>
        </div>

        {statusState === "verifying" && (
          <div className="auth-loading-state" style={{ minHeight: "140px" }}>
            <div className="auth-spinner" />
            <p>Validating verification token...</p>
          </div>
        )}

        {statusState === "success" && (
          <div>
            <div className="auth-alert auth-alert-success" role="alert">
              <span className="auth-alert-icon">✓</span>
              <span>{statusMessage}</span>
            </div>
            <Link to="/login" className="btn-brand-solid" style={{ width: "100%", justifyContent: "center", marginTop: "20px" }}>
              Sign In to Your Workspace
            </Link>
          </div>
        )}

        {statusState === "error" && (
          <div>
            <div className="auth-alert auth-alert-error" role="alert">
              <span className="auth-alert-icon">⚠️</span>
              <span>{statusMessage}</span>
            </div>
            <p style={{ fontSize: "13.5px", color: "var(--text-secondary)", marginBottom: "16px" }}>
              You can request a new verification email below:
            </p>
          </div>
        )}

        {(statusState === "idle" || statusState === "error") && (
          <form onSubmit={handleResend} style={{ marginTop: "12px" }}>
            <FormInput
              id="resend-email"
              label="Account Email"
              type="email"
              value={resendEmail}
              onChange={(e) => setResendEmail(e.target.value)}
              placeholder="name@company.com"
              required
              disabled={resending}
            />

            {resendMessage && (
              <div className="auth-alert auth-alert-success" style={{ marginTop: "10px" }}>
                <span>{resendMessage}</span>
              </div>
            )}

            <button
              type="submit"
              className="btn-secondary-outline"
              style={{ width: "100%", marginTop: "10px" }}
              disabled={resending || !resendEmail}
            >
              {resending ? "Sending..." : "Resend Verification Link"}
            </button>
          </form>
        )}

        <div className="auth-footer">
          <Link to="/">Back to Home</Link>
        </div>
      </div>
    </div>
  );
}
