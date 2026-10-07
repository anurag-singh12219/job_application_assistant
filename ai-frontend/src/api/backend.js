import axios from "axios";

// Base API URL configuration
const getApiBaseUrl = () => {
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL;
  }
  // In dev mode with Vite dev proxy, empty string uses same-origin proxy
  if (import.meta.env.DEV) {
    return "";
  }
  if (typeof window !== "undefined" && window.location?.hostname) {
    return `http://${window.location.hostname}:8000`;
  }
  return "http://localhost:8000";
};

// In-memory access token storage (strictly memory only; never in localStorage)
let inMemoryAccessToken = null;

export function setAccessToken(token) {
  inMemoryAccessToken = token || null;
}

export function getAccessToken() {
  return inMemoryAccessToken;
}

const API = axios.create({
  baseURL: getApiBaseUrl(),
  withCredentials: true // Transmit and store secure HttpOnly cookies
});

// Helper to extract cookie value by name
export function getCookie(name) {
  if (typeof document === "undefined") return null;
  const match = document.cookie.match(new RegExp("(^|;\\s*)" + name + "=([^;]*)"));
  return match ? decodeURIComponent(match[2]) : null;
}

// Request interceptor: Attach Authorization header and anti-CSRF token
API.interceptors.request.use((config) => {
  if (inMemoryAccessToken) {
    config.headers["Authorization"] = `Bearer ${inMemoryAccessToken}`;
  }

  const method = config.method?.toLowerCase();
  if (["post", "put", "patch", "delete"].includes(method)) {
    const csrfToken = getCookie("csrf_token");
    if (csrfToken) {
      config.headers["X-CSRF-Token"] = csrfToken;
    }
  }
  return config;
}, (error) => Promise.reject(error));

// Response interceptor: Handle 401s and attempt silent token rotation once
let isRefreshing = false;
let failedQueue = [];

const processQueue = (error) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve();
    }
  });
  failedQueue = [];
};

API.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // Ignore refresh endpoint itself to avoid infinite loop
    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      !originalRequest.url?.includes("/api/auth/refresh") &&
      !originalRequest.url?.includes("/api/auth/login") &&
      !originalRequest.url?.includes("/api/auth/register")
    ) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then(() => API(originalRequest))
          .catch((err) => Promise.reject(err));
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        const refreshRes = await API.post("/api/auth/refresh");
        if (refreshRes.data?.access_token) {
          setAccessToken(refreshRes.data.access_token);
          originalRequest.headers["Authorization"] = `Bearer ${refreshRes.data.access_token}`;
        }
        processQueue(null);
        return API(originalRequest);
      } catch (refreshError) {
        setAccessToken(null);
        processQueue(refreshError);
        window.dispatchEvent(new CustomEvent("auth:session-expired"));
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

// =================== AUTHENTICATION API ===================

export const authAPI = {
  getCsrfToken: async () => {
    const response = await API.get("/api/auth/csrf-token");
    return response.data;
  },

  register: async (payload) => {
    const response = await API.post("/api/auth/register", payload);
    return response.data;
  },

  login: async (credentials) => {
    const response = await API.post("/api/auth/login", credentials);
    if (response.data?.access_token) {
      setAccessToken(response.data.access_token);
    }
    return response.data;
  },

  logout: async () => {
    setAccessToken(null);
    const response = await API.post("/api/auth/logout");
    return response.data;
  },

  refresh: async () => {
    const response = await API.post("/api/auth/refresh");
    if (response.data?.access_token) {
      setAccessToken(response.data.access_token);
    }
    return response.data;
  },

  getCurrentUser: async () => {
    const response = await API.get("/api/auth/me");
    return response.data;
  },

  forgotPassword: async (email) => {
    const response = await API.post("/api/auth/forgot-password", { email });
    return response.data;
  },

  resetPassword: async (data) => {
    const response = await API.post("/api/auth/reset-password", data);
    return response.data;
  },

  verifyEmail: async (token) => {
    const response = await API.post("/api/auth/verify-email", { token });
    return response.data;
  },

  resendVerification: async (email) => {
    const response = await API.post("/api/auth/resend-verification", { email });
    return response.data;
  },

  changePassword: async (data) => {
    const response = await API.patch("/api/auth/change-password", data);
    return response.data;
  }
};

// =================== ADMINISTRATION API ===================

export const adminAPI = {
  getAdminMe: async () => {
    const response = await API.get("/api/admin/me");
    return response.data;
  },

  getUsers: async (params = {}) => {
    const response = await API.get("/api/admin/users", { params });
    return response.data;
  },

  updateUserStatus: async (userId, isActive) => {
    const response = await API.patch(`/api/admin/users/${userId}/status`, { is_active: isActive });
    return response.data;
  },

  updateUserRole: async (userId, role) => {
    const response = await API.patch(`/api/admin/users/${userId}/role`, { role });
    return response.data;
  }
};

// =================== EXISTING CAREER ASSISTANT API ===================

export const analyzeResume = async (formData) => {
  const response = await API.post("/analyze", formData);
  return response.data;
};

export const generateCoverLetter = async (data) => {
  const response = await API.post("/cover-letter/quick", {
    user_name: data.userName || "Candidate",
    job_title: data.jobTitle,
    company_name: data.companyName,
    skills: data.skills,
    experience_years: parseInt(data.experienceYears, 10) || 0
  });
  return response.data;
};

export const getInterviewPrep = async (data) => {
  const response = await API.post("/interview-prep", data);
  return response.data;
};

export const getSalaryInsights = async (data) => {
  const response = await API.post("/salary-insights", data);
  return response.data;
};

export const searchJobs = async (data) => {
  const response = await API.post("/jobs/search", data);
  return response.data;
};

export const searchInternships = async (keywords, location) => {
  const response = await API.post("/internships/search", { keywords, location });
  return response.data;
};

export const getCareerAdvice = async (data) => {
  const response = await API.post("/chat", data);
  return response.data;
};

export const getCareerAdviceWithFile = async (formData) => {
  const response = await API.post("/chat/with-file", formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });
  return response.data;
};

export default API;
