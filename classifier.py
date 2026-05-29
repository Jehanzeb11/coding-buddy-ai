import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline

MODEL_PATH = "persona_classifier.pkl"

# Training data: user questions and their best persona match
TRAINING_DATA = [
    # Assistant queries
    ("How do I write a function?", "assistant"),
    ("What's the best practice for error handling?", "assistant"),
    ("Show me how to implement this feature", "assistant"),
    ("Can you help me with this code?", "assistant"),
    
    # Explainer queries
    ("Can you explain this code?", "explainer"),
    ("Break down this algorithm step by step", "explainer"),
    ("What does this function do?", "explainer"),
    ("Explain how this works in simple terms", "explainer"),
    
    # Reviewer queries
    ("Review my code for bugs", "reviewer"),
    ("Check this for security issues", "reviewer"),
    ("Is this code well-written?", "reviewer"),
    ("Analyze this code for improvements", "reviewer"),
    
    # Debugger queries
    ("Why is my code not working?", "debugger"),
    ("This throws an error, help me fix it", "debugger"),
    ("There's a bug in my code", "debugger"),
    ("My program crashes here", "debugger"),
]

def train_classifier():
    """Train Decision Tree classifier"""
    texts = [data[0] for data in TRAINING_DATA]
    labels = [data[1] for data in TRAINING_DATA]
    
    clf = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('dt', DecisionTreeClassifier(max_depth=5, random_state=42))
    ])
    clf.fit(texts, labels)
    
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(clf, f)
    print("Decision Tree classifier trained and saved!")

def predict_persona(text):
    """Predict the best persona for given text"""
    try:
        if not os.path.exists(MODEL_PATH):
            train_classifier()
        
        with open(MODEL_PATH, 'rb') as f:
            clf = pickle.load(f)
        
        return clf.predict([text])[0]
    except Exception as e:
        print(f"Error in predict_persona: {e}")
        return "assistant"  # Fallback to default
