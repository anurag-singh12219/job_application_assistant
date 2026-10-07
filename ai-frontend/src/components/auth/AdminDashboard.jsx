import { useState, useEffect, useCallback } from "react";
import { adminAPI } from "../../api/backend";
import { useAuth } from "../../context/AuthContext";
import "./Auth.css";

export default function AdminDashboard() {
  const { user: currentAdmin } = useAuth();
  const [users, setUsers] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [actionLoadingId, setActionLoadingId] = useState(null);
  const [feedback, setFeedback] = useState(null);

  const fetchUsers = useCallback(async (searchQuery = "") => {
    try {
      setLoading(true);
      const data = await adminAPI.getUsers({
        skip: 0,
        limit: 50,
        search: searchQuery || undefined
      });
      setUsers(data.users || []);
      setTotal(data.total || 0);
    } catch (err) {
      const detail = err.response?.data?.detail;
      setFeedback({ type: "error", message: detail || "Failed to load user management directory." });
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchUsers(search);
  }, [fetchUsers, search]);

  const handleToggleStatus = async (user) => {
    if (user.id === currentAdmin.id && user.is_active) {
      setFeedback({ type: "error", message: "You cannot deactivate your own administrator account." });
      return;
    }

    const nextStatus = !user.is_active;
    setActionLoadingId(user.id);
    setFeedback(null);

    try {
      const updated = await adminAPI.updateUserStatus(user.id, nextStatus);
      setUsers((prev) => prev.map((u) => (u.id === user.id ? updated : u)));
      setFeedback({
        type: "success",
        message: `Account for ${user.email} is now ${nextStatus ? "active" : "suspended"}.`
      });
    } catch (err) {
      const detail = err.response?.data?.detail;
      setFeedback({ type: "error", message: detail || "Failed to update account status." });
    } finally {
      setActionLoadingId(null);
    }
  };

  const handleRoleChange = async (user, newRole) => {
    if (user.id === currentAdmin.id && newRole !== "admin") {
      setFeedback({ type: "error", message: "Administrators cannot demote themselves." });
      return;
    }

    setActionLoadingId(user.id);
    setFeedback(null);

    try {
      const updated = await adminAPI.updateUserRole(user.id, newRole);
      setUsers((prev) => prev.map((u) => (u.id === user.id ? updated : u)));
      setFeedback({
        type: "success",
        message: `Role for ${user.email} updated to '${newRole}'.`
      });
    } catch (err) {
      const detail = err.response?.data?.detail;
      setFeedback({ type: "error", message: detail || "Failed to update user role." });
    } finally {
      setActionLoadingId(null);
    }
  };

  return (
    <div className="admin-container">
      <div className="admin-header-row">
        <div>
          <h1 className="profile-name">Administrator Control Center</h1>
          <p style={{ color: "var(--text-secondary)", fontSize: "14px" }}>
            Role-Based Access Control and user administration ({total} registered {total === 1 ? "user" : "users"})
          </p>
        </div>

        <input
          type="text"
          className="admin-search-input"
          placeholder="Search by name or email..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {feedback && (
        <div
          className={`auth-alert ${feedback.type === "error" ? "auth-alert-error" : "auth-alert-success"}`}
          role="alert"
        >
          <span className="auth-alert-icon">{feedback.type === "error" ? "⚠️" : "✓"}</span>
          <span>{feedback.message}</span>
        </div>
      )}

      <div className="admin-table-card">
        {loading ? (
          <div className="auth-loading-state" style={{ padding: "40px 0" }}>
            <div className="auth-spinner" />
            <p>Loading directory...</p>
          </div>
        ) : users.length === 0 ? (
          <div style={{ padding: "40px", textAlign: "center", color: "var(--text-muted)" }}>
            No users matched the criteria.
          </div>
        ) : (
          <div style={{ overflowX: "auto" }}>
            <table className="admin-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>User</th>
                  <th>Role</th>
                  <th>Status</th>
                  <th>Verification</th>
                  <th>Created</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {users.map((u) => (
                  <tr key={u.id}>
                    <td>#{u.id}</td>
                    <td>
                      <div style={{ fontWeight: 600 }}>{u.full_name}</div>
                      <div style={{ fontSize: "12px", color: "var(--text-secondary)" }}>{u.email}</div>
                    </td>
                    <td>
                      <select
                        className="admin-select-role"
                        value={u.role}
                        onChange={(e) => handleRoleChange(u, e.target.value)}
                        disabled={actionLoadingId === u.id || u.id === currentAdmin.id}
                        aria-label={`Change role for ${u.full_name}`}
                      >
                        <option value="user">User</option>
                        <option value="admin">Admin</option>
                      </select>
                    </td>
                    <td>
                      <span
                        className={`profile-badge ${
                          u.is_active ? "badge-verified" : "badge-unverified"
                        }`}
                      >
                        {u.is_active ? "Active" : "Suspended"}
                      </span>
                    </td>
                    <td>
                      <span
                        className={`profile-badge ${
                          u.is_email_verified ? "badge-verified" : "badge-unverified"
                        }`}
                      >
                        {u.is_email_verified ? "Verified" : "Unverified"}
                      </span>
                    </td>
                    <td style={{ fontSize: "12.5px", color: "var(--text-muted)" }}>
                      {new Date(u.created_at).toLocaleDateString()}
                    </td>
                    <td>
                      <button
                        type="button"
                        className={`admin-btn-action ${
                          u.is_active ? "admin-btn-toggle-active" : "admin-btn-toggle-restore"
                        }`}
                        onClick={() => handleToggleStatus(u)}
                        disabled={actionLoadingId === u.id || u.id === currentAdmin.id}
                      >
                        {actionLoadingId === u.id
                          ? "..."
                          : u.is_active
                          ? "Suspend"
                          : "Activate"}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
