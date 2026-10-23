# FinMate AI: An Intelligent Personal Finance Chatbot with Expense Classification, Budget Optimization, and Predictive Analytics

Team ArthX | MCA Project

## Abstract
FinMate AI is a Streamlit-based personal finance assistant. Users record income and
expenses manually or via CSV; the system classifies expense descriptions using a
TF-IDF and Logistic Regression pipeline, answers supported questions through an
intent-based chatbot whose numbers come from deterministic code, tracks budgets and
savings goals, flags statistically unusual expenses, runs what-if simulations, and
produces monthly expense forecasts. Amounts are stored as integer paise, passwords
are hashed with bcrypt, and every query is scoped to the authenticated user. On a
250-row educational dataset the classifier reached about 0.74 cross-validated
accuracy against a 0.60 rule-based baseline; these figures are optimistic because the
data is self-written. The project is educational and is not financial advice.

## Problem Statement
Individuals often do not track spending consistently, categorise transactions by hand,
and cannot easily ask questions about their own records. FinMate AI provides a low-cost
local tool that combines record keeping, simple machine learning and transparent
calculations.

## Aim and Objectives
1. Build a secure multi-user finance tracker (SQLite, bcrypt, user-scoped queries).
2. Classify expense descriptions with a measurable ML model and a fallback.
3. Provide a closed-domain chatbot using intent recognition and entity extraction.
4. Support budgets, savings goals, what-if simulation and anomaly flags.
5. Forecast monthly expenses and compare against a baseline using chronological evaluation.
6. Verify behaviour with automated tests.