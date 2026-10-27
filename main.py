import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("КІПЗс-25-3 - Основи Програмування(1).csv")
df = df.dropna(subset=["Прізвище та ініціали студентів"]).copy()

date_cols = ["09.09.2026",
             "12.09.2026",
             "25.09.2026",
             "02.10.2026",
             "09.10.2026",
             "16.10.2026"
]

for col in date_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["Середній бал"] = df[date_cols].mean(axis=1).round(2)
group_mean = np.nanmean(df[date_cols].to_numpy())
all_grades = df[date_cols].to_numpy()
max_grade = np.nanmax(all_grades)
min_grade = np.nanmin(all_grades)

df["Оцінок 1-3"] = (df[date_cols] <= 3).sum(axis=1)
df["Статус"] = np.where(df["Середній бал"] <7, "потребує уваги", "Добре")

sum_df = df[
    ["Прізвище та ініціали студентів", "Середній бал", "Оцінок 1–3", "Статус"]
]

print(sum_df.head())