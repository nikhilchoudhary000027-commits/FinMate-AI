import pandas as pd
from modules.forecasting import evaluate

df = pd.read_csv("data/synthetic_monthly_expenses.csv")
series = pd.Series(df["expense_rupees"].values, index=df["month"])

r = evaluate(series)
print("SYNTHETIC data | train months:", r["train_months"], "| test months:", r["test_months"])
print(f"Baseline  MAE {r['baseline_mae']:.0f}  RMSE {r['baseline_rmse']:.0f}")
print(f"Model     MAE {r['model_mae']:.0f}  RMSE {r['model_rmse']:.0f}")