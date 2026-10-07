import { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";

import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";
import Chat from "./components/Chat";
import ResumeAnalysis from "./components/ResumeAnalysis";
import CoverLetter from "./components/CoverLetter";
import InterviewPrep from "./components/InterviewPrep";
import SalaryNegotiation from "./components/SalaryNegotiation";
import JobSearch from "./components/JobSearch";
import CommandPalette from "./components/CommandPalette";

import Login from "./components/auth/Login";
import Register from "./components/auth/Register";
import ForgotPassword from "./components/auth/ForgotPassword";
import ResetPassword from "./components/auth/ResetPassword";
import VerifyEmail from "./components/auth/VerifyEmail";
import Profile from "./components/auth/Profile";
import AdminDashboard from "./components/auth/AdminDashboard";
import Unauthorized from "./components/auth/Unauthorized";
import ProtectedRoute from "./components/auth/ProtectedRoute";
import AdminRoute from "./components/auth/AdminRoute";

import "./styles/theme.css";
import "./App.css";

function AppShell() {
  const [activeView, setActiveView] = useState("home");
  const [chatHistory, setChatHistory] = useState([]);
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const navigate = useNavigate();

  // Initialize theme: saved in localStorage -> system preference -> default dark
  const [theme, setTheme] = useState(() => {
    const saved = localStorage.getItem("jobai_theme");
    if (saved === "light" || saved === "dark") {
      return saved;
    }
    if (typeof window !== "undefined" && window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches) {
      return "light";
    }
    return "dark"; // Default is dark
  });

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("jobai_theme", theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === "dark" ? "light" : "dark"));
  };

  // Keyboard shortcut Ctrl+K / Cmd+K to open search modal
  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setIsSearchOpen((prev) => !prev);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  const handleNewSession = () => {
    navigate("/");
    setActiveView("chat");
    window.dispatchEvent(new CustomEvent("newChat"));
  };

  const handleSelectView = (viewId) => {
    navigate("/");
    setActiveView(viewId);
  };

  return (
    <div className="app-root">
      {/* Ambient background lighting & hexagon watermark */}
      <div className="ambient-background" aria-hidden="true">
        <div className="ambient-glow-warm" />
        <div className="ambient-glow-purple" />
        <div className="ambient-hex-grid" />
      </div>

      {/* Top Navigation Bar */}
      <Navbar
        activeView={activeView}
        setActiveView={handleSelectView}
        theme={theme}
        toggleTheme={toggleTheme}
        onOpenSearch={() => setIsSearchOpen(true)}
        onNewSession={handleNewSession}
      />

      <Routes>
        {/* Main Application Workspace with Sidebar */}
        <Route
          path="/"
          element={
            <div className="app-body">
              <Sidebar activeView={activeView} setActiveView={handleSelectView} />
              <main className="main-content-area" id="main-content">
                <WorkspaceView
                  activeView={activeView}
                  setActiveView={handleSelectView}
                  chatHistory={chatHistory}
                  setChatHistory={setChatHistory}
                  onOpenSearch={() => setIsSearchOpen(true)}
                />
              </main>
            </div>
          }
        />

        {/* Authentication Routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="/verify-email" element={<VerifyEmail />} />
        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <Profile />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin"
          element={
            <AdminRoute>
              <AdminDashboard />
            </AdminRoute>
          }
        />
        <Route path="/unauthorized" element={<Unauthorized />} />

        {/* Catch-all redirect */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>

      {/* Quick Switcher / Command Palette */}
      <CommandPalette
        isOpen={isSearchOpen}
        onClose={() => setIsSearchOpen(false)}
        onSelectView={handleSelectView}
      />
    </div>
  );
}

function WorkspaceView({ activeView, setActiveView, chatHistory, setChatHistory, onOpenSearch }) {
  switch (activeView) {
    case "chat":
      return <Chat chatHistory={chatHistory} setChatHistory={setChatHistory} />;
    case "resume":
      return <ResumeAnalysis />;
    case "cover-letter":
      return <CoverLetter />;
    case "interview":
      return <InterviewPrep />;
    case "salary":
      return <SalaryNegotiation />;
    case "jobs":
      return <JobSearch />;
    default:
      return <HomeView setActiveView={setActiveView} onOpenSearch={onOpenSearch} />;
  }
}

function HomeView({ setActiveView, onOpenSearch }) {
  const featureCards = [
    {
      id: "resume",
      icon: "📄",
      colorClass: "accent-coral",
      title: "Analyze Resume",
      desc: "Get instant feedback on your resume and ATS score",
      arrow: "→"
    },
    {
      id: "cover-letter",
      icon: "✍️",
      colorClass: "accent-emerald",
      title: "Write Cover Letter",
      desc: "Generate personalized cover letters with AI",
      arrow: "→"
    },
    {
      id: "interview",
      icon: "💬",
      colorClass: "accent-gold",
      title: "Interview Prep",
      desc: "Practice with AI-generated interview questions",
      arrow: "→"
    },
    {
      id: "salary",
      icon: "💵",
      colorClass: "accent-purple",
      title: "Salary Negotiation",
      desc: "Get market insights and negotiation strategies",
      arrow: "→"
    },
    {
      id: "jobs",
      icon: "🎯",
      colorClass: "accent-cyan",
      title: "Job Search Strategy",
      desc: "Find jobs and internships matching your skills",
      arrow: "→"
    },
    {
      id: "chat",
      icon: "💼",
      colorClass: "accent-indigo",
      title: "Career Advice",
      desc: "Chat with AI for personalized career guidance",
      arrow: "→"
    }
  ];

  return (
    <div className="home-dashboard-view">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <div className="hero-badge">
            <span className="hero-badge-dot" />
            <span>AI CAREER COPILOT</span>
          </div>

          <h1 className="hero-display-heading">
            <span className="hero-heading-line-1">
              Accelerate Your <span className="hero-heading-gradient">Career</span>
            </span>
            <span className="hero-heading-line-2">land your dream job with AI</span>
          </h1>

          <p className="hero-subtitle">
            Get expert help with resumes, cover letters, interview prep, and salary insights.
            Let's land your dream job together.
          </p>

          {/* Prominent floating search pill */}
          <div className="hero-search-wrapper">
            <button className="hero-search-pill" onClick={onOpenSearch} aria-label="Search tools and questions">
              <svg className="hero-search-icon" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="8.5" cy="8.5" r="5.5" />
                <path d="M13 13l4 4" strokeLinecap="round" />
              </svg>
              <span className="hero-search-placeholder">Search tools, resume tips, interview questions...</span>
              <kbd className="hero-search-kbd">Ctrl K</kbd>
            </button>
          </div>

          {/* Feature Tags Pill Row */}
          <div className="hero-feature-tags" aria-label="Key features">
            <span className="hero-tag" onClick={() => setActiveView("resume")}>✨ Resume Analysis</span>
            <span className="hero-tag" onClick={() => setActiveView("cover-letter")}>📝 Cover Letters</span>
            <span className="hero-tag" onClick={() => setActiveView("interview")}>🎤 Interview Prep</span>
            <span className="hero-tag" onClick={() => setActiveView("salary")}>💰 Salary Negotiation</span>
            <span className="hero-tag" onClick={() => setActiveView("resume")}>⚡ ATS Optimization</span>
            <span className="hero-tag" onClick={() => setActiveView("jobs")}>🎯 Job Search</span>
          </div>
        </div>
      </section>

      {/* Feature Cards Grid */}
      <section className="quick-start-section">
        <div className="section-header-centered">
          <h2 className="section-title">Quick Start</h2>
          <p className="section-subtitle">
            Explore the AI-powered tools designed to make your job application fast, sharp, and successful.
          </p>
        </div>

        <div className="dockkit-cards-grid">
          {featureCards.map((card) => (
            <button
              key={card.id}
              className={`dockkit-card ${card.colorClass}`}
              onClick={() => setActiveView(card.id)}
            >
              <div className="dockkit-card-icon-box">
                <span className="dockkit-card-icon">{card.icon}</span>
              </div>
              <h3 className="dockkit-card-title">{card.title}</h3>
              <p className="dockkit-card-desc">{card.desc}</p>
              <div className="dockkit-card-footer">
                <span className="dockkit-card-arrow">{card.arrow}</span>
              </div>
            </button>
          ))}
        </div>
      </section>

      {/* Statistics Metrics Section */}
      <section className="stats-section-modern">
        <div className="stat-card-modern">
          <div className="stat-number-modern">10K+</div>
          <div className="stat-label-modern">Users Helped</div>
          <p className="stat-detail-modern">Job seekers landed interviews worldwide</p>
        </div>
        <div className="stat-card-modern highlight">
          <div className="stat-number-modern gradient-text">95%</div>
          <div className="stat-label-modern">Success Rate</div>
          <p className="stat-detail-modern">Improved ATS compatibility and response</p>
        </div>
        <div className="stat-card-modern">
          <div className="stat-number-modern">24/7</div>
          <div className="stat-label-modern">Available</div>
          <p className="stat-detail-modern">Instant feedback without waiting</p>
        </div>
      </section>

      {/* Call to Action Section */}
      <section className="cta-banner-modern">
        <div className="cta-banner-content">
          <div className="cta-icon-badge">💼</div>
          <h2>Ready to Get Started?</h2>
          <p>Supercharge your job application today with our state-of-the-art AI assistant.</p>
          <button className="btn-brand-solid" onClick={() => setActiveView("resume")}>
            Start Your Resume Analysis Now →
          </button>
        </div>
      </section>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppShell />
      </BrowserRouter>
    </AuthProvider>
  );
}
