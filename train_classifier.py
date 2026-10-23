"""Train and evaluate the expense classifier (TF-IDF + Logistic Regression)."""

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from modules.categorization import rule_based_category

df = pd.read_csv("data/expense_training_data.csv")

# Stratified split keeps every category in both train and test sets.
X_train, X_test, y_train, y_test = train_test_split(
    df["description"], df["category"],
    test_size=0.25, random_state=42, stratify=df["category"],
)
print("Train size:", len(X_train), "| Test size:", len(X_test))

# ---- Baseline: manual rules (not machine learning) ----
baseline_pred = [rule_based_category(text) for text in X_test]
print("\nRule-based baseline accuracy:", round(accuracy_score(y_test, baseline_pred), 3))

# ---- ML model ----
model = Pipeline([
    ("tfidf", TfidfVectorizer(lowercase=True, ngram_range=(1, 2))),
    ("clf", LogisticRegression(C=10, max_iter=2000)),
])
model.fit(X_train, y_train)
pred = model.predict(X_test)

print("ML model accuracy:", round(accuracy_score(y_test, pred), 3))
print("\nClassification report:\n")
print(classification_report(y_test, pred, zero_division=0))

labels = sorted(df["category"].unique())
print("Confusion matrix (rows = actual, columns = predicted):")
print(pd.DataFrame(confusion_matrix(y_test, pred, labels=labels),
                   index=labels, columns=labels))

# ---- Save the trained pipeline ----
joblib.dump(model, "models/expense_classifier.joblib")
print("\nModel saved to models/expense_classifier.joblib")