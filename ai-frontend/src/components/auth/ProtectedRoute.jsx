import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import "./Auth.css";

export default function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="auth-loading-state">
        <div className="auth-spinner" />
        <p>Verifying secure session...</p>
      </div>
    );
  }

  if (!user) {
    // Preserve intended deep-link path
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
}
