import pandas as pd

df = pd.read_csv("data/intent_training_data.csv")
print("Rows:", len(df))
print(df["intent"].value_counts())
print("Missing:", df.isna().sum().sum())