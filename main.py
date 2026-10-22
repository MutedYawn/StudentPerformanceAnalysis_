import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("КІПЗс-25-3 - Основи Програмування.csv")
df = df.dropna(subset=["Прізвище та ініціали студентів"])

columns_needed = ["Прізвище та ініціали студентів", "01.10", "03.10", "05.10"]
df_filtered = df[columns_needed]

for col in df_filtered.columns[1:]:
    df_filtered[col] = pd.to_numeric(df_filtered[col], errors="coerce")

df_filtered["01.10"] = pd.to_numeric(df_filtered["01.10"], errors="coerce")

df_clean = df_filtered.copy()
print("--- Перші 5 рядків чистої таблиці ---")
print(df_clean.head())

print(f"\nРозмір чистої таблиці (рядки, стовпці): {df_clean.shape}")
print("\nНазви колонок у df_clean:", list(df_clean.columns))