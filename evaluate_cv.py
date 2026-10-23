"""5-fold stratified cross-validation for the expense classifier."""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline

df = pd.read_csv("data/expense_training_data.csv")

model = Pipeline([
    ("tfidf", TfidfVectorizer(lowercase=True, ngram_range=(1, 2))),
    ("clf", LogisticRegression(max_iter=1000)),
])

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, df["description"], df["category"], cv=cv, scoring="accuracy")

print("Fold accuracies:", [round(s, 3) for s in scores])
print("Mean accuracy:", round(scores.mean(), 3))
print("Std deviation:", round(scores.std(), 3))