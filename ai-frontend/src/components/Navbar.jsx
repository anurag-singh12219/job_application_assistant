import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "./Navbar.css";

export default function Navbar({ activeView, setActiveView, theme, toggleTheme, onOpenSearch, onNewSession }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const { user, isAdmin, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  // Close mobile menu on resize to desktop
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth > 900) {
        setMobileMenuOpen(false);
      }
    };
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const navLinks = [
    { id: "home", label: "Home" },
    { id: "resume", label: "Resume Analysis" },
    { id: "cover-letter", label: "Cover Letter" },
    { id: "interview", label: "Interview Prep" },
    { id: "salary", label: "Salary" },
    { id: "jobs", label: "Job Search" },
    { id: "chat", label: "AI Chat" }
  ];

  const handleNavClick = (viewId) => {
    navigate("/");
    if (setActiveView) {
      setActiveView(viewId);
    }
    setMobileMenuOpen(false);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleLogout = async () => {
    await logout();
    navigate("/login");
  };

  const initials = user?.full_name
    ? user.full_name.split(" ").map((n) => n[0]).join("").toUpperCase().slice(0, 2)
    : "U";

  return (
    <>
      <header className={`top-navbar ${scrolled ? "scrolled" : ""}`}>
        <div className="navbar-container">
          {/* Brand Logo & Title */}
          <div className="navbar-brand" onClick={() => handleNavClick("home")} role="button" tabIndex={0} aria-label="Go to homepage">
            <div className="brand-logo-icon">
              <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" className="brand-svg">
                <defs>
                  <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#f97316" />
                    <stop offset="50%" stopColor="#ec4899" />
                    <stop offset="100%" stopColor="#8b5cf6" />
                  </linearGradient>
                </defs>
                <rect x="1" y="1" width="30" height="30" rx="9" fill="var(--bg-surface)" stroke="url(#logoGrad)" strokeWidth="2" />
                <rect x="8" y="11" width="16" height="3" rx="1.5" fill="currentColor" />
                <rect x="8" y="18" width="10" height="3" rx="1.5" fill="currentColor" opacity="0.85" />
              </svg>
            </div>
            <span className="brand-title">JobPilot<span className="brand-badge">AI</span></span>
          </div>

          {/* Desktop Navigation Links */}
          <nav className="desktop-nav-links" aria-label="Main Navigation">
            {navLinks.map((link) => (
              <button
                key={link.id}
                className={`nav-link-btn ${activeView === link.id ? "active" : ""}`}
                onClick={() => handleNavClick(link.id)}
              >
                {link.label}
              </button>
            ))}
          </nav>

          {/* Right Actions */}
          <div className="navbar-actions">
            {/* Quick Search Shortcut Pill */}
            <button
              className="nav-search-btn"
              onClick={onOpenSearch}
              title="Search tools & features (Ctrl+K)"
              aria-label="Open search dialog"
            >
              <svg className="search-icon" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="8.5" cy="8.5" r="5.5" />
                <path d="M13 13l4 4" strokeLinecap="round" />
              </svg>
              <span className="search-text">Search...</span>
              <kbd className="search-kbd">Ctrl K</kbd>
            </button>

            {/* Theme Toggle Pill */}
            <button
              className="theme-toggle-pill"
              onClick={toggleTheme}
              title={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}
              aria-label={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}
              type="button"
            >
              <span className="theme-toggle-thumb" />
              <div className="theme-toggle-icons">
                <span className="theme-toggle-icon sun">
                  <svg viewBox="0 0 16 16" fill="currentColor" width="12" height="12">
                    <path d="M8 12a4 4 0 100-8 4 4 0 000 8zM8 0a1 1 0 011 1v1a1 1 0 11-2 0V1a1 1 0 011-1zm0 13a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zm8-6a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM3 8a1 1 0 01-1 1H1a1 1 0 110-2h1a1 1 0 011 1zm9.657-5.657a1 1 0 010 1.414l-.707.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zm-8.485 8.485a1 1 0 010 1.414l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 0zm8.485 0a1 1 0 011.414 0l.707.707a1 1 0 01-1.414 1.414l-.707-.707a1 1 0 010-1.414zm-8.485-8.485a1 1 0 011.414 0l.707.707a1 1 0 01-1.414 1.414l-.707-.707a1 1 0 010-1.414z" />
                  </svg>
                </span>
                <span className="theme-toggle-icon moon">
                  <svg viewBox="0 0 16 16" fill="currentColor" width="12" height="12">
                    <path d="M6 .278a.768.768 0 01.08.858 7.208 7.208 0 00-.878 3.46c0 4.021 3.278 7.277 7.318 7.277.527 0 1.04-.055 1.533-.16a.787.787 0 01.81.316.733.733 0 01-.031.893A8.349 8.349 0 018.344 16C3.734 16 0 12.286 0 7.71 0 4.266 2.114 1.312 5.124.06A.752.752 0 016 .278z" />
                  </svg>
                </span>
              </div>
            </button>

            {/* Authentication States */}
            {user ? (
              <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                {isAdmin && (
                  <Link to="/admin" className="nav-admin-link-btn" title="Administrator Control Center">
                    <span>Admin</span>
                  </Link>
                )}

                <button
                  type="button"
                  className="nav-user-chip"
                  onClick={() => navigate("/profile")}
                  title="View your profile & settings"
                >
                  <span className="nav-user-avatar">{initials}</span>
                  <span>{user.full_name?.split(" ")[0] || "User"}</span>
                </button>

                <button
                  type="button"
                  className="btn-dockkit-cta nav-cta-btn"
                  onClick={onNewSession}
                  title="Start a new career analysis session"
                >
                  <span>+ New Session</span>
                </button>
              </div>
            ) : (
              <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <Link to="/login" className="nav-signin-btn">
                  Sign In
                </Link>

                <Link to="/register" className="btn-dockkit-cta nav-cta-btn">
                  <span>Get Started</span>
                </Link>
              </div>
            )}

            {/* Mobile Hamburger Toggle */}
            <button
              className="mobile-hamburger-btn"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              aria-label={mobileMenuOpen ? "Close menu" : "Open menu"}
              aria-expanded={mobileMenuOpen}
            >
              <span className={`hamburger-bar ${mobileMenuOpen ? "open" : ""}`} />
              <span className={`hamburger-bar ${mobileMenuOpen ? "open" : ""}`} />
              <span className={`hamburger-bar ${mobileMenuOpen ? "open" : ""}`} />
            </button>
          </div>
        </div>
      </header>

      {/* Mobile Drawer Menu */}
      <div className={`mobile-drawer-overlay ${mobileMenuOpen ? "open" : ""}`} onClick={() => setMobileMenuOpen(false)}>
        <aside className={`mobile-drawer ${mobileMenuOpen ? "open" : ""}`} onClick={(e) => e.stopPropagation()}>
          <div className="mobile-drawer-header">
            <div className="navbar-brand">
              <div className="brand-logo-icon">
                <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" className="brand-svg">
                  <rect x="1" y="1" width="30" height="30" rx="9" fill="var(--bg-surface)" stroke="url(#logoGrad)" strokeWidth="2" />
                  <rect x="8" y="11" width="16" height="3" rx="1.5" fill="currentColor" />
                  <rect x="8" y="18" width="10" height="3" rx="1.5" fill="currentColor" opacity="0.85" />
                </svg>
              </div>
              <span className="brand-title">JobPilot<span className="brand-badge">AI</span></span>
            </div>
            <button className="mobile-close-btn" onClick={() => setMobileMenuOpen(false)} aria-label="Close menu">
              ✕
            </button>
          </div>

          <div className="mobile-drawer-search">
            <button className="mobile-search-btn" onClick={() => { setMobileMenuOpen(false); onOpenSearch(); }}>
              <svg className="search-icon" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="8.5" cy="8.5" r="5.5" />
                <path d="M13 13l4 4" strokeLinecap="round" />
              </svg>
              <span>Quick Search (Ctrl+K)</span>
            </button>
          </div>

          <nav className="mobile-nav-list">
            {navLinks.map((link) => (
              <button
                key={link.id}
                className={`mobile-nav-item ${activeView === link.id ? "active" : ""}`}
                onClick={() => handleNavClick(link.id)}
              >
                <span>{link.label}</span>
                {activeView === link.id && <span className="active-dot" />}
              </button>
            ))}

            <div style={{ height: "1px", background: "var(--border-subtle)", margin: "10px 0" }} />

            {user ? (
              <>
                <button
                  className="mobile-nav-item"
                  onClick={() => { setMobileMenuOpen(false); navigate("/profile"); }}
                >
                  <span>Profile ({user.full_name})</span>
                </button>
                {isAdmin && (
                  <button
                    className="mobile-nav-item"
                    onClick={() => { setMobileMenuOpen(false); navigate("/admin"); }}
                  >
                    <span>Admin Control Center</span>
                  </button>
                )}
                <button
                  className="mobile-nav-item"
                  onClick={() => { setMobileMenuOpen(false); handleLogout(); }}
                >
                  <span style={{ color: "var(--error)" }}>Sign Out</span>
                </button>
              </>
            ) : (
              <>
                <button
                  className="mobile-nav-item"
                  onClick={() => { setMobileMenuOpen(false); navigate("/login"); }}
                >
                  <span>Sign In</span>
                </button>
                <button
                  className="mobile-nav-item"
                  onClick={() => { setMobileMenuOpen(false); navigate("/register"); }}
                >
                  <span style={{ color: "var(--brand-orange)", fontWeight: 700 }}>Create Free Account</span>
                </button>
              </>
            )}
          </nav>

          <div className="mobile-drawer-footer">
            <div className="mobile-theme-row">
              <span className="mobile-theme-label">Theme Mode: {theme === "dark" ? "Dark" : "Light"}</span>
              <button
                className="theme-toggle-pill"
                onClick={toggleTheme}
                aria-label={`Switch theme`}
              >
                <span className="theme-toggle-thumb" />
                <div className="theme-toggle-icons">
                  <span className="theme-toggle-icon sun">☀️</span>
                  <span className="theme-toggle-icon moon">🌙</span>
                </div>
              </button>
            </div>
          </div>
        </aside>
      </div>
    </>
  );
}
