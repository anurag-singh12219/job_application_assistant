import axios from "axios";

// Use environment variable for production, fallback to localhost for development
const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

// Debug: Log the API URL being used
console.log("[Backend Config] API URL:", API_URL);
console.log("[Backend Config] Environment:", import.meta.env.MODE);

const API = axios.create({
  baseURL: API_URL
});

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
    experience_years: parseInt(data.experienceYears) || 0
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

