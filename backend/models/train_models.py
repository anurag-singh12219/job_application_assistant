import pandas as pd
import pickle
import os

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# Load training data
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "../training_data.csv")
df = pd.read_csv(data_path)

# Create pipeline (vectorizer + classifier)
model = Pipeline([
    ("vectorizer", CountVectorizer()),
    ("classifier", MultinomialNB())
])

# Train model
model.fit(df["skills"], df["role"])

# Save trained model
model_path = os.path.join(script_dir, "role_model.pkl")
with open(model_path, "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved as role_model.pkl")
