import { useState } from "react";
import "./Sidebar.css";

export default function Sidebar({ activeView, setActiveView }) {
  const [isExpanded, setIsExpanded] = useState(true);

  const menuItems = [
    { id: "home", icon: "🏠", label: "Home" },
    { id: "resume", icon: "📄", label: "Resume Analysis" },
    { id: "cover-letter", icon: "✍️", label: "Cover Letter" },
    { id: "interview", icon: "💬", label: "Interview Prep" },
    { id: "salary", icon: "💰", label: "Salary Negotiation" },
    { id: "jobs", icon: "🎯", label: "Job Search" },
    { id: "chat", icon: "🤖", label: "AI Chat" }
  ];

  return (
    <aside className={`sidebar ${isExpanded ? "expanded" : "collapsed"}`}>
      <div className="sidebar-header">
        <div className="logo">
          <span className="logo-icon">🤖</span>
          {isExpanded && <span className="logo-text">JobBot</span>}
        </div>
        <button 
          className="toggle-btn"
          onClick={() => setIsExpanded(!isExpanded)}
        >
          {isExpanded ? "◀" : "▶"}
        </button>
      </div>

      <button 
        className="new-chat-btn"
        onClick={() => setActiveView("chat")}
      >
        <span>+</span>
        {isExpanded && <span>New Chat</span>}
      </button>

      <nav className="sidebar-nav">
        {menuItems.map(item => (
          <button
            key={item.id}
            className={`nav-item ${activeView === item.id ? "active" : ""}`}
            onClick={() => setActiveView(item.id)}
          >
            <span className="nav-icon">{item.icon}</span>
            {isExpanded && <span className="nav-label">{item.label}</span>}
          </button>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div className="ai-badge">
          <span className="ai-icon">⚡</span>
          {isExpanded && (
            <div>
              <div className="ai-badge-title">AI-Powered</div>
              <div className="ai-badge-text">Advanced career assistance with AI</div>
            </div>
          )}
        </div>
      </div>
    </aside>
  );
}
