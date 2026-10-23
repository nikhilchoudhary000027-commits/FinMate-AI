import pandas as pd

df = pd.read_csv("data/expense_training_data.csv")
print("Rows:", len(df))
print(df["category"].value_counts())
print("Missing values:", df.isna().sum().sum())