import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("journal.csv")

dates = df[["09.09.2026", "12.09.2026", "25.09.2026", "02.10.2026", "09.10.2026", "16.10.2026"]]
arr = dates.to_numpy(dtype=float)

df["Середній бал"] = dates.mean(axis=1).round(1)
df["Оцінок 1-3"] = ((arr >= 1) & (arr <= 3)).sum(axis=1)
df["Статус"] = np.where(df["Середній бал"] >= 7, "Добре", "Потребує уваги")

df_summary = df[["ПІБ", "Середній бал", "Оцінок 1-3", "Статус"]]
df_summary.to_csv("results.csv", index=False, encoding="utf-8-sig")

print(df)
print("Середній бал:", np.nanmean(arr))
print("Найвищий бал:", np.nanmax(arr))
print("Найнижчий бал:", np.nanmin(arr))

colors = ['red' if score < 7 else 'skyblue' for score in df_summary['Середній бал']]

plt.bar(df_summary['ПІБ'], df_summary["Середній бал"], color=colors,edgecolor="black")
plt.savefig("average_grades.png")
plt.show()

group_means = dates.mean(axis=0)

min_date = group_means.idxmin()
min_val = group_means.min()
print(f"Дата з найнижчим середнім балом: {min_date} ({min_val:.2f})")

plt.figure(figsize=(10, 5))
plt.plot(group_means.index, group_means.values, marker='o', color='tab:blue', linewidth=2, linestyle='-')

plt.title("Динаміка успішності групи", fontsize=12, fontweight="bold")
plt.xlabel("Дата заняття")
plt.ylabel("Середній бал")
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("performance_trend.png")
plt.show()

grades = arr[~np.isnan(arr)]

counts, bins, patches = plt.hist(grades, bins=range(1, 14), align='left', edgecolor="black")

for i in range(3):
    patches[i].set_facecolor('red')

top_grade = int(bins[np.argmax(counts)])
plt.title(f"Розподіл оцінок. Найчастіша: {top_grade}")
plt.savefig("grades_distribution.png")
plt.show()

students_scores = list(zip(df_summary["ПІБ"], df_summary["Середній бал"]))

def insertion_sort(data):
    arr_copy = data.copy()
    for i in range(1, len(arr_copy)):
        key = arr_copy[i]
        j = i - 1
        
        while j >= 0 and arr_copy[j][1] > key[1]:
            arr_copy[j + 1] = arr_copy[j]
            j -= 1
        arr_copy[j + 1] = key
    return arr_copy

sorted_custom = insertion_sort(students_scores)

print("\nTop 5 найнижчих балів <Insertion Sort>")
for name, score in sorted_custom[:5]:
    print(f"{name}: {score}")
sorted_builtin = sorted(students_scores, key=lambda x: x[1])

print("\nРезультати збігаються з sorted():", sorted_custom == sorted_builtin)