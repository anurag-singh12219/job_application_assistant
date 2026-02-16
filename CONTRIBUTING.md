# Contributing to AI Job Application Assistant

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Bugs

Found a bug? Please create an issue with:
- Clear, descriptive title
- Step-by-step reproduction instructions
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)

**Example:**
```
Title: Resume upload fails with PDF containing images

Steps:
1. Upload a PDF resume with embedded images
2. Click "Analyze"

Expected: Resume analyzed successfully
Actual: Error "Failed to extract text from PDF"

Environment: Windows 10, Python 3.12, Chrome browser
```

### Suggesting Features

Have a feature idea? Open an issue with:
- Clear description of the feature
- Use cases and why it would be useful
- Any alternative approaches you've considered

**Example:**
```
Feature: Export resume critique as PDF

Use case: Users want to download detailed feedback as a professional PDF report
This would help them share results with mentors or keep records.
```

### Submitting Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/job_application_assistant.git
   cd job_application_assistant
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/add-export-pdf
   ```

3. **Make your changes**
   - Keep commits focused and descriptive
   - Follow existing code style
   - Add comments for complex logic
   - Test your changes thoroughly

4. **Install development dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

5. **Run tests**
   ```bash
   pytest
   # or run the application
   uvicorn main:app --reload --port 8000
   ```

6. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add PDF export for resume critique"
   ```
   Use conventional commits:
   - `feat:` new feature
   - `fix:` bug fix
   - `docs:` documentation
   - `style:` code style (no functional change)
   - `refactor:` refactoring code
   - `test:` adding tests
   - `chore:` build/dependency changes

7. **Push to your fork**
   ```bash
   git push origin feature/add-export-pdf
   ```

8. **Create a Pull Request**
   - Go to https://github.com/anurag-singh12219/job_application_assistant
   - Click "New Pull Request"
   - Ensure base repository is `anurag-singh12219/job_application_assistant`
   - Provide clear description of changes

---

## Development Setup

### Backend

```bash
cd backend

# Virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Run server
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd ai-frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

---

## Code Style

### Python
- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions
- Keep lines under 100 characters
- Use type hints where possible

**Example:**
```python
def calculate_ats_score(resume_text: str, job_description: str) -> float:
    """
    Calculate ATS score using TF-IDF vectorization.
    
    Args:
        resume_text: Resume content as string
        job_description: Job description content
        
    Returns:
        ATS score from 0-100
    """
    # Implementation here
    pass
```

### JavaScript/React
- Use ES6+ syntax
- Use meaningful component names
- Add comments for complex logic
- Keep components focused and reusable

**Example:**
```javascript
// ResumeAnalysis.jsx
export function ResumeAnalysis() {
  // Component logic
  return (
    <div className="resume-analysis">
      {/* JSX content */}
    </div>
  );
}
```

---

## Testing

### Backend Tests
```bash
cd backend
pytest tests/  # Run all tests
pytest tests/test_ats_engine.py  # Run specific test
pytest -v  # Verbose output
```

### Frontend Testing
```bash
cd ai-frontend
npm test  # Run tests
npm run build  # Build check
```

---

## Documentation

When contributing code, update documentation:
- Update README.md if adding features
- Update DOCUMENTATION.md if changing algorithms
- Update API_REFERENCE.md if modifying endpoints
- Add inline code comments for complex logic

---

## Areas for Contribution

### High Priority
- [ ] Improve job matching algorithm accuracy
- [ ] Add database support (PostgreSQL)
- [ ] Improve resume parsing for different formats
- [ ] Add more salary data points
- [ ] Implement caching layer (Redis)

### Medium Priority
- [ ] Add more interview question categories
- [ ] Expand skill database
- [ ] Better error handling
- [ ] Performance optimizations
- [ ] Mobile app improvements

### Low Priority
- [ ] Additional themes
- [ ] Internationalization (i18n)
- [ ] Advanced analytics
- [ ] Social features

---

## Review Process

PRs will be reviewed within 48 hours. Reviewers will check:
- Code quality and style
- Documentation completeness
- Test coverage
- Functionality and performance
- Security implications

Please be patient and open to feedback!

---

## Questions?

- Check existing issues: https://github.com/anurag-singh12219/job_application_assistant/issues
- Read DOCUMENTATION.md for technical details
- Open an issue for discussion

---

**Thank you for contributing! 🙏**
