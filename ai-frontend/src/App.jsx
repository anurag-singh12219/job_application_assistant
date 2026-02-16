import { useState } from "react";
import Sidebar from "./components/Sidebar";
import Chat from "./components/Chat";
import ResumeAnalysis from "./components/ResumeAnalysis";
import CoverLetter from "./components/CoverLetter";
import InterviewPrep from "./components/InterviewPrep";
import SalaryNegotiation from "./components/SalaryNegotiation";
import JobSearch from "./components/JobSearch";
import "./styles/theme.css";
import "./App.css";

function App() {
  const [activeView, setActiveView] = useState("home");
  const [chatHistory, setChatHistory] = useState([]);

  const renderContent = () => {
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
        return <HomeView setActiveView={setActiveView} />;
    }
  };

  return (
    <div className="app-container">
      <Sidebar activeView={activeView} setActiveView={setActiveView} />
      <main className="main-content">
        {renderContent()}
      </main>
    </div>
  );
}

function HomeView({ setActiveView }) {
  return (
    <div className="home-view">
      <div className="home-header">
        <div className="header-content">
          <h1>🚀 Your AI Career Assistant</h1>
          <p>Get expert help with resumes, cover letters, interview prep, and more. Let's land your dream job together.</p>
        </div>
        <div className="header-illustration">
          <div className="illustration-icon">💼</div>
        </div>
      </div>

      <div className="feature-tags">
        <span className="feature-tag">✨ Resume Analysis</span>
        <span className="feature-tag">📝 Cover Letters</span>
        <span className="feature-tag">🎤 Interview Prep</span>
        <span className="feature-tag">💰 Salary Negotiation</span>
        <span className="feature-tag">⚡ ATS Optimization</span>
      </div>

      <div className="quick-start">
        <h2>Quick Start</h2>
        <div className="quick-start-grid">
          <button className="quick-start-card resume-card" onClick={() => setActiveView("resume")}>
            <div className="card-icon">📄</div>
            <h3>Analyze Resume</h3>
            <p>Get instant feedback on your resume and ATS score</p>
            <span className="card-arrow">→</span>
          </button>

          <button className="quick-start-card letter-card" onClick={() => setActiveView("cover-letter")}>
            <div className="card-icon">✍️</div>
            <h3>Write Cover Letter</h3>
            <p>Generate personalized cover letters with AI</p>
            <span className="card-arrow">→</span>
          </button>

          <button className="quick-start-card interview-card" onClick={() => setActiveView("interview")}>
            <div className="card-icon">💬</div>
            <h3>Interview Prep</h3>
            <p>Practice with AI-generated interview questions</p>
            <span className="card-arrow">→</span>
          </button>

          <button className="quick-start-card salary-card" onClick={() => setActiveView("salary")}>
            <div className="card-icon">💵</div>
            <h3>Salary Negotiation</h3>
            <p>Get market insights and negotiation strategies</p>
            <span className="card-arrow">→</span>
          </button>

          <button className="quick-start-card jobs-card" onClick={() => setActiveView("jobs")}>
            <div className="card-icon">🎯</div>
            <h3>Job Search Strategy</h3>
            <p>Find jobs and internships matching your skills</p>
            <span className="card-arrow">→</span>
          </button>

          <button className="quick-start-card chat-card" onClick={() => setActiveView("chat")}>
            <div className="card-icon">💼</div>
            <h3>Career Advice</h3>
            <p>Chat with AI for personalized career guidance</p>
            <span className="card-arrow">→</span>
          </button>
        </div>
      </div>

      <div className="stats-section">
        <div className="stat-item">
          <div className="stat-number">10K+</div>
          <div className="stat-label">Users Helped</div>
        </div>
        <div className="stat-item">
          <div className="stat-number">95%</div>
          <div className="stat-label">Success Rate</div>
        </div>
        <div className="stat-item">
          <div className="stat-number">24/7</div>
          <div className="stat-label">Available</div>
        </div>
      </div>

      <div className="cta-section">
        <h2>Ready to Get Started?</h2>
        <button className="btn-primary-lg" onClick={() => setActiveView("resume")}>
          Start Your Resume Analysis Now
        </button>
      </div>
    </div>
  );
}

export default App;
