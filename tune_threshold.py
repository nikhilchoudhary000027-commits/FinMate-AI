"""Compare C values and show accuracy at different confidence thresholds."""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline

df = pd.read_csv("data/expense_training_data.csv")
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

for C in [1, 10, 50]:
    model = Pipeline([
        ("tfidf", TfidfVectorizer(lowercase=True, ngram_range=(1, 2))),
        ("clf", LogisticRegression(C=C, max_iter=2000)),
    ])
    proba = cross_val_predict(model, df["description"], df["category"],
                              cv=cv, method="predict_proba")
    classes = np.array(sorted(df["category"].unique()))
    pred = classes[proba.argmax(axis=1)]
    conf = proba.max(axis=1)
    correct = pred == df["category"].values

    print(f"\nC = {C} | overall accuracy = {correct.mean():.3f}")
    for t in [0.2, 0.3, 0.4, 0.5, 0.6]:
        mask = conf >= t
        if mask.sum() == 0:
            continue
        print(f"  threshold {t}: kept {mask.mean():.0%} of rows, "
              f"accuracy on kept = {correct[mask].mean():.3f}")