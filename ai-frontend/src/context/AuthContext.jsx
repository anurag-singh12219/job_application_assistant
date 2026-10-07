/* eslint-disable react-refresh/only-export-components */
import { createContext, useState, useEffect, useCallback } from "react";
import { authAPI } from "../api/backend";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Initialize and check current user session on mount
  const checkAuth = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      // Initialize CSRF token
      try {
        await authAPI.getCsrfToken();
      } catch {
        // Silently continue if csrf endpoint isn't reached yet
      }

      const userData = await authAPI.getCurrentUser();
      setUser(userData);
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    checkAuth();

    // Listen for session expiration events from the Axios interceptor
    const handleSessionExpired = () => {
      setUser(null);
    };

    window.addEventListener("auth:session-expired", handleSessionExpired);
    return () => window.removeEventListener("auth:session-expired", handleSessionExpired);
  }, [checkAuth]);

  const login = async (email, password, rememberMe = false) => {
    setError(null);
    const data = await authAPI.login({
      email,
      password,
      remember_me: rememberMe
    });
    setUser(data.user);
    return data;
  };

  const register = async (payload) => {
    setError(null);
    const data = await authAPI.register(payload);
    // User is created; if auto-logged-in or verification required, state can be refreshed
    return data;
  };

  const logout = async () => {
    try {
      await authAPI.logout();
    } catch (err) {
      console.warn("Logout request failed:", err);
    } finally {
      setUser(null);
    }
  };

  const refreshUser = async () => {
    try {
      const userData = await authAPI.getCurrentUser();
      setUser(userData);
      return userData;
    } catch {
      setUser(null);
      return null;
    }
  };

  const value = {
    user,
    loading,
    error,
    isAuthenticated: !!user,
    isAdmin: user?.role === "admin",
    login,
    register,
    logout,
    checkAuth,
    refreshUser,
    setError
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export { AuthContext };
export { useAuth } from "./useAuth";
