import { useEffect, useRef, useState } from "react";
import "./CommandPalette.css";

const tools = [
  {
    id: "resume",
    icon: "📄",
    title: "Resume Analysis & ATS Scoring",
    description: "Scan your resume against job descriptions for ATS score, skill match, and gaps",
    category: "Analysis"
  },
  {
    id: "cover-letter",
    icon: "✍️",
    title: "AI Cover Letter Generator",
    description: "Draft bespoke, impactful cover letters tailored to your target company and skills",
    category: "Writing"
  },
  {
    id: "interview",
    icon: "💬",
    title: "Interview Preparation & Practice",
    description: "AI-generated technical, behavioral (STAR method), and counter-questions",
    category: "Preparation"
  },
  {
    id: "salary",
    icon: "💰",
    title: "Salary Insights & Negotiation",
    description: "Market compensation benchmarks, negotiation strategies, and leverage points",
    category: "Strategy"
  },
  {
    id: "jobs",
    icon: "🎯",
    title: "Job & Internship Search",
    description: "Live opportunities matched to your profile and preferred locations",
    category: "Search"
  },
  {
    id: "chat",
    icon: "🤖",
    title: "AI Career Copilot Chat",
    description: "24/7 personalized career guidance, document Q&A, and career transitions",
    category: "Assistant"
  },
  {
    id: "home",
    icon: "🏠",
    title: "Home Dashboard",
    description: "Return to overview, quick stats, and application launchpad",
    category: "Navigation"
  }
];

export default function CommandPalette({ isOpen, onClose, onSelectView }) {
  const [query, setQuery] = useState("");
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef(null);

  const filtered = tools.filter((tool) =>
    tool.title.toLowerCase().includes(query.toLowerCase()) ||
    tool.description.toLowerCase().includes(query.toLowerCase()) ||
    tool.category.toLowerCase().includes(query.toLowerCase())
  );

  useEffect(() => {
    if (isOpen) {
      const timer = setTimeout(() => {
        inputRef.current?.focus();
      }, 50);
      return () => clearTimeout(timer);
    }
  }, [isOpen]);

  const handleInputChange = (e) => {
    setQuery(e.target.value);
    setSelectedIndex(0);
  };

  const handleKeyDown = (e) => {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setSelectedIndex((prev) => (prev + 1) % (filtered.length || 1));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setSelectedIndex((prev) => (prev - 1 + filtered.length) % (filtered.length || 1));
    } else if (e.key === "Enter" && filtered[selectedIndex]) {
      e.preventDefault();
      handleSelect(filtered[selectedIndex].id);
    } else if (e.key === "Escape") {
      e.preventDefault();
      handleClose();
    }
  };

  const handleClose = () => {
    setQuery("");
    setSelectedIndex(0);
    onClose();
  };

  const handleSelect = (viewId) => {
    onSelectView(viewId);
    handleClose();
  };

  if (!isOpen) return null;

  return (
    <div className="cmd-backdrop" onClick={handleClose} role="dialog" aria-modal="true" aria-label="Command palette">
      <div className="cmd-modal" onClick={(e) => e.stopPropagation()}>
        <div className="cmd-header">
          <svg className="cmd-search-icon" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="8.5" cy="8.5" r="5.5" />
            <path d="M13 13l4 4" strokeLinecap="round" />
          </svg>
          <input
            ref={inputRef}
            type="text"
            className="cmd-input"
            placeholder="Type a command, tool name, or feature..."
            value={query}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
          />
          <kbd className="cmd-esc-kbd" onClick={handleClose}>ESC</kbd>
        </div>

        <div className="cmd-list">
          {filtered.length > 0 ? (
            filtered.map((item, idx) => (
              <div
                key={item.id}
                className={`cmd-item ${idx === selectedIndex ? "selected" : ""}`}
                onClick={() => handleSelect(item.id)}
                onMouseEnter={() => setSelectedIndex(idx)}
              >
                <span className="cmd-item-icon">{item.icon}</span>
                <div className="cmd-item-info">
                  <div className="cmd-item-title-row">
                    <span className="cmd-item-title">{item.title}</span>
                    <span className="cmd-item-category">{item.category}</span>
                  </div>
                  <span className="cmd-item-desc">{item.description}</span>
                </div>
                <span className="cmd-item-arrow">↵</span>
              </div>
            ))
          ) : (
            <div className="cmd-empty">
              <p>No matching features found for "{query}"</p>
            </div>
          )}
        </div>

        <div className="cmd-footer">
          <span>Navigate with <kbd>↑</kbd> <kbd>↓</kbd></span>
          <span>Select with <kbd>↵ Enter</kbd></span>
          <span>Close with <kbd>Esc</kbd></span>
        </div>
      </div>
    </div>
  );
}
