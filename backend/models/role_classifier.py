import pickle
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "role_model.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

def predict_role(skills):
    skills_text = " ".join(skills)
    prediction = model.predict([skills_text])[0]
    return prediction
