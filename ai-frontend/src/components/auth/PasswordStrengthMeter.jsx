import "./Auth.css";

export default function PasswordStrengthMeter({ password = "" }) {
  if (!password) return null;

  const checks = [
    { label: "At least 8 characters", valid: password.length >= 8 },
    { label: "At least 1 uppercase letter", valid: /[A-Z]/.test(password) },
    { label: "At least 1 lowercase letter", valid: /[a-z]/.test(password) },
    { label: "At least 1 number", valid: /\d/.test(password) },
    { label: "At least 1 special character", valid: /[^A-Za-z0-9]/.test(password) }
  ];

  const passedCount = checks.filter((c) => c.valid).length;

  let strengthLabel = "Too Weak";
  let strengthClass = "strength-weak";

  if (passedCount >= 5) {
    strengthLabel = "Strong";
    strengthClass = "strength-strong";
  } else if (passedCount >= 4) {
    strengthLabel = "Good";
    strengthClass = "strength-good";
  } else if (passedCount >= 2) {
    strengthLabel = "Fair";
    strengthClass = "strength-fair";
  }

  return (
    <div className="password-strength-container" aria-live="polite">
      <div className="strength-header">
        <span className="strength-text">Password Strength:</span>
        <span className={`strength-badge ${strengthClass}`}>{strengthLabel}</span>
      </div>

      <div className="strength-bars">
        {[1, 2, 3, 4, 5].map((index) => (
          <div
            key={index}
            className={`strength-bar-segment ${
              index <= passedCount ? strengthClass : "strength-empty"
            }`}
          />
        ))}
      </div>

      <ul className="strength-checklist">
        {checks.map((check, idx) => (
          <li key={idx} className={`checklist-item ${check.valid ? "passed" : "pending"}`}>
            <span className="checklist-icon">{check.valid ? "✓" : "○"}</span>
            <span>{check.label}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
