import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { authAPI } from "../../api/backend";
import FormInput from "./FormInput";
import PasswordStrengthMeter from "./PasswordStrengthMeter";
import "./Auth.css";

export default function Profile() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmNewPassword, setConfirmNewPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const handlePasswordChange = async (e) => {
    e.preventDefault();
    setErrorMessage("");
    setStatusMessage("");

    if (!currentPassword || !newPassword) {
      setErrorMessage("Please complete all password fields.");
      return;
    }
    if (newPassword.length < 8) {
      setErrorMessage("New password must be at least 8 characters long.");
      return;
    }
    if (newPassword !== confirmNewPassword) {
      setErrorMessage("New passwords do not match.");
      return;
    }

    setLoading(true);
    try {
      const data = await authAPI.changePassword({
        current_password: currentPassword,
        new_password: newPassword,
        confirm_new_password: confirmNewPassword
      });
      setStatusMessage(data.message || "Password changed successfully! Please log in again.");
      setCurrentPassword("");
      setNewPassword("");
      setConfirmNewPassword("");
      setTimeout(() => {
        logout();
        navigate("/login");
      }, 2500);
    } catch (err) {
      const detail = err.response?.data?.detail;
      setErrorMessage(detail || "Failed to update password. Please check your current password.");
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    await logout();
    navigate("/login");
  };

  if (!user) return null;

  const initials = user.full_name
    ? user.full_name.split(" ").map((n) => n[0]).join("").toUpperCase().slice(0, 2)
    : "U";

  return (
    <div className="profile-container">
      {/* Header Profile Card */}
      <div className="profile-header-card">
        <div className="profile-user-info">
          <div className="profile-avatar-circle">{initials}</div>
          <div>
            <h1 className="profile-name">{user.full_name}</h1>
            <div className="profile-email">
              <span>{user.email}</span>
              <span className={`profile-badge ${user.role === "admin" ? "badge-admin" : "badge-user"}`}>
                {user.role}
              </span>
              <span className={`profile-badge ${user.is_email_verified ? "badge-verified" : "badge-unverified"}`}>
                {user.is_email_verified ? "Verified" : "Unverified"}
              </span>
            </div>
          </div>
        </div>

        <button
          type="button"
          className="btn-secondary-outline"
          onClick={handleLogout}
        >
          Sign Out
        </button>
      </div>

      <div className="profile-grid">
        {/* Account Details Card */}
        <div className="profile-card">
          <h2 className="profile-card-title">Security & Account Status</h2>
          <div style={{ display: "flex", flexDirection: "column", gap: "14px", fontSize: "14px" }}>
            <div>
              <strong style={{ color: "var(--text-secondary)", display: "block", fontSize: "12.5px" }}>User ID</strong>
              <span>#{user.id}</span>
            </div>
            <div>
              <strong style={{ color: "var(--text-secondary)", display: "block", fontSize: "12.5px" }}>Assigned Role</strong>
              <span style={{ textTransform: "capitalize" }}>{user.role}</span>
            </div>
            <div>
              <strong style={{ color: "var(--text-secondary)", display: "block", fontSize: "12.5px" }}>Account Created</strong>
              <span>{new Date(user.created_at).toLocaleDateString(undefined, { year: "numeric", month: "long", day: "numeric" })}</span>
            </div>
            <div>
              <strong style={{ color: "var(--text-secondary)", display: "block", fontSize: "12.5px" }}>Session Protection</strong>
              <span style={{ color: "var(--success)" }}>✓ Encrypted HttpOnly Cookies with Refresh Rotation</span>
            </div>
          </div>
        </div>

        {/* Change Password Card */}
        <div className="profile-card">
          <h2 className="profile-card-title">Change Password</h2>

          {statusMessage && (
            <div className="auth-alert auth-alert-success" role="alert">
              <span className="auth-alert-icon">✓</span>
              <span>{statusMessage}</span>
            </div>
          )}

          {errorMessage && (
            <div className="auth-alert auth-alert-error" role="alert">
              <span className="auth-alert-icon">⚠️</span>
              <span>{errorMessage}</span>
            </div>
          )}

          <form onSubmit={handlePasswordChange}>
            <FormInput
              id="profile-current-pass"
              label="Current Password"
              type="password"
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
              placeholder="••••••••"
              required
              disabled={loading}
            />

            <FormInput
              id="profile-new-pass"
              label="New Password"
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              placeholder="••••••••"
              required
              disabled={loading}
            />

            <PasswordStrengthMeter password={newPassword} />

            <FormInput
              id="profile-confirm-new-pass"
              label="Confirm New Password"
              type="password"
              value={confirmNewPassword}
              onChange={(e) => setConfirmNewPassword(e.target.value)}
              placeholder="••••••••"
              required
              disabled={loading}
            />

            <button
              type="submit"
              className="auth-submit-btn"
              disabled={loading || !currentPassword || !newPassword}
            >
              {loading ? "Updating..." : "Update Password"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
