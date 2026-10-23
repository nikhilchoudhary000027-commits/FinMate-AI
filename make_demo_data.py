"""Generate a clearly-labelled SYNTHETIC monthly expense series for forecasting demos."""

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
months = pd.period_range("2024-01", periods=30, freq="M")

# Synthetic pattern: base spending + slow growth + festive spikes + noise.
base = 22000
trend = np.arange(30) * 150
festive = np.array([3000 if m.month in (10, 11, 12) else 0 for m in months])
noise = rng.normal(0, 1200, 30)

expense_rupees = (base + trend + festive + noise).round(0)

df = pd.DataFrame({"month": months.astype(str), "expense_rupees": expense_rupees})
df.to_csv("data/synthetic_monthly_expenses.csv", index=False)
print("SYNTHETIC data written:", len(df), "months")
print(df.head())
print(df.tail())