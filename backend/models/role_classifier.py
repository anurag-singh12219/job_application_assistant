import pickle
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "role_model.pkl")

# Load model if available, otherwise use fallback
model = None
try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    print(f"[Warning] Model file not found at {MODEL_PATH}. Role prediction will use fallback.")
except Exception as e:
    print(f"[Warning] Failed to load model: {e}. Role prediction will use fallback.")

def predict_role(skills):
    """Predict job role based on skills. Falls back to simple heuristics if model unavailable."""
    if model is None:
        # Fallback: simple keyword-based prediction
        skills_lower = " ".join(skills).lower()
        if any(word in skills_lower for word in ["python", "java", "javascript", "programming"]):
            return "Software Developer"
        elif any(word in skills_lower for word in ["data", "analysis", "sql", "statistics"]):
            return "Data Analyst"
        elif any(word in skills_lower for word in ["design", "ui", "ux", "figma"]):
            return "Designer"
        elif any(word in skills_lower for word in ["marketing", "seo", "content"]):
            return "Marketing Specialist"
        else:
            return "Professional"
    
    # Use ML model if available
    skills_text = " ".join(skills)
    prediction = model.predict([skills_text])[0]
    return prediction
