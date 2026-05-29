import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline

MODEL_PATH = "decision_tree_model.pkl"

# Training data - questions mapped to personas
TRAINING_DATA = [
    ("How do I write a function?", "assistant"),
    ("Can you explain this code?", "explainer"),
    ("Review my code for bugs", "reviewer"),
    ("Why is my code not working?", "debugger"),
    ("What's the best practice for error handling?", "assistant"),
    ("Break down this algorithm step by step", "explainer"),
    ("Check this for security issues", "reviewer"),
    ("This throws an error, help me fix it", "debugger"),
    ("How do I use this library?", "assistant"),
    ("What does this function do?", "explainer"),
    ("Is this code optimized?", "reviewer"),
    ("Where is the bug in this code?", "debugger"),
    ("Show me an example", "assistant"),
    ("Simplify this for me", "explainer"),
    ("Find performance issues", "reviewer"),
    ("Fix this crash", "debugger"),
]

def train_decision_tree():
    """Train Decision Tree classifier on persona data"""
    texts = [data[0] for data in TRAINING_DATA]
    labels = [data[1] for data in TRAINING_DATA]
    
    clf = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=50)),
        ('dt', DecisionTreeClassifier(max_depth=10, random_state=42))
    ])
    clf.fit(texts, labels)
    
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(clf, f)
    print("Decision Tree classifier trained and saved!")

def predict_persona(text):
    """Predict the best persona for given text"""
    if not os.path.exists(MODEL_PATH):
        train_decision_tree()
    
    with open(MODEL_PATH, 'rb') as f:
        clf = pickle.load(f)
    
    return clf.predict([text])[0]
