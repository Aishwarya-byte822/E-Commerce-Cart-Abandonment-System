import pandas as pd

df = pd.read_csv("2019-Nov.csv", nrows=5)
print("Columns: ")
print(df.columns.tolist())
print("\nSample Data:")
print(df.head())