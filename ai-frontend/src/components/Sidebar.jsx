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

  const handleNewSession = () => {
    setActiveView("chat");
    window.dispatchEvent(new CustomEvent("newChat"));
  };

  return (
    <aside className={`app-sidebar ${isExpanded ? "expanded" : "collapsed"}`} aria-label="Sidebar navigation">
      <div className="sidebar-top">
        <div className="sidebar-brand-section">
          {isExpanded && (
            <div className="sidebar-brand-label">
              <span className="brand-dot" />
              <span>WORKSPACE</span>
            </div>
          )}
          <button
            className="sidebar-collapse-btn"
            onClick={() => setIsExpanded(!isExpanded)}
            title={isExpanded ? "Collapse sidebar" : "Expand sidebar"}
            aria-label={isExpanded ? "Collapse sidebar" : "Expand sidebar"}
          >
            <svg
              className={`collapse-icon ${isExpanded ? "" : "rotated"}`}
              viewBox="0 0 20 20"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <path d="M12 15l-5-5 5-5" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </button>
        </div>

        {/* New Session Action */}
        <button
          className="sidebar-new-btn"
          onClick={handleNewSession}
          title="Start a new analysis or chat session"
        >
          <span className="new-btn-icon">+</span>
          {isExpanded && <span className="new-btn-label">New Session</span>}
        </button>
      </div>

      {/* Navigation List */}
      <nav className="sidebar-nav-menu">
        {menuItems.map((item) => {
          const isActive = activeView === item.id;
          return (
            <button
              key={item.id}
              className={`sidebar-nav-item ${isActive ? "active" : ""}`}
              onClick={() => setActiveView(item.id)}
              title={!isExpanded ? item.label : undefined}
              aria-current={isActive ? "page" : undefined}
            >
              <span className="sidebar-item-icon">{item.icon}</span>
              {isExpanded && <span className="sidebar-item-label">{item.label}</span>}
              {isActive && <span className="sidebar-active-indicator" />}
            </button>
          );
        })}
      </nav>

      {/* Sidebar Footer */}
      <div className="sidebar-bottom">
        <div className="sidebar-ai-card">
          <div className="ai-status-indicator">
            <span className="status-pulse" />
          </div>
          {isExpanded && (
            <div className="ai-status-details">
              <div className="ai-status-heading">AI Engine Online</div>
              <div className="ai-status-sub">GPT-4 & Career Insights</div>
            </div>
          )}
        </div>
      </div>
    </aside>
  );
}
