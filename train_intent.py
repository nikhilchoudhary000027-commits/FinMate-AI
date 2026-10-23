"""Train and evaluate the chatbot intent classifier."""

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline

df = pd.read_csv("data/intent_training_data.csv")


def build_model():
    return Pipeline([
        ("tfidf", TfidfVectorizer(lowercase=True, ngram_range=(1, 2))),
        ("clf", LogisticRegression(C=10, max_iter=2000)),
    ])


# Out-of-fold predictions: every row is predicted by a model that never saw it.
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
pred = cross_val_predict(build_model(), df["text"], df["intent"], cv=cv)
print("Cross-validated accuracy:", round((pred == df["intent"]).mean(), 3))
print()
print(classification_report(df["intent"], pred, zero_division=0))

# Final model trained on all rows for the app.
final_model = build_model().fit(df["text"], df["intent"])
joblib.dump(final_model, "models/intent_classifier.joblib")
print("Saved models/intent_classifier.joblib")