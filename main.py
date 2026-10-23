import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("КІПЗс-25-3 - Основи Програмування.csv")
df = df.dropna(subset=["Прізвище та ініціали студентів"])

columns_needed = df[["09.09.2026","12.09.2026","25.09.2026","02.10.2026","09.10.2026","16.10.2026"]].to_numpy()
df_filtered = df[columns_needed]

for col in df_filtered.columns[1:]:
    df_filtered[col] = pd.to_numeric(df_filtered[col], errors="coerce")

df["середнє"] = df[["09.09.2026","12.09.2026","25.09.2026","02.10.2026","09.10.2026","16.10.2026"]].mean(axis=1)
print(df)
ultimate_grade = np.mean(df["середнє"], axis=0)
print(ultimate_grade)

df_max = df[["09.09.2026","12.09.2026","25.09.2026","02.10.2026","09.10.2026","16.10.2026"]].max(axis=1)

print(df_max.head())
