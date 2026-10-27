import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Крок 1. Завантаження та аналіз структури файлу
df_raw = pd.read_csv("КІПЗс-25-3 - Основи програмування.csv", header=None)

# У вашому журналі рядок 4 містить дати занять
header_row_idx = 4
dates_row = df_raw.iloc[header_row_idx].values

date_columns_indices = []
date_column_names = []

for idx, val in enumerate(dates_row):
    if pd.notna(val) and "." in str(val) and len(str(val).strip()) >= 8:
        date_columns_indices.append(idx)
        date_column_names.append(str(val).strip())

# Збираємо дані студентів починаючи з 5-го рядка
students_data = []
row_idx = 5
while row_idx < len(df_raw):
    student_name = df_raw.iloc[row_idx, 1]  # Стовпець 1 — ПІБ
    if pd.isna(student_name) or "Прізвище" in str(student_name):
        row_idx += 1
        continue
    row_grades = [df_raw.iloc[row_idx, c_idx] for c_idx in date_columns_indices]
    students_data.append([student_name] + row_grades)
    row_idx += 1

columns_list = ["ПІБ"] + date_column_names
df_clean = pd.DataFrame(students_data, columns=columns_list)

print("--- Крок 1: Перші 5 рядків журналу ---")
print(df_clean.head())
print(f"Кількість студентів: {len(df_clean)}, Кількість стовпців: {df_clean.shape[1]}")

# Крок 2. Очищення даних (Pandas)
grades_df = df_clean[date_column_names].apply(
    lambda col: pd.to_numeric(col, errors="coerce")
)
grades_matrix = grades_df.to_numpy()

# Крок 3. Аналіз успішності (NumPy + Pandas)
student_names = df_clean["ПІБ"].values
student_means = np.nanmean(grades_matrix, axis=1)
student_means_safe = np.nan_to_num(student_means, nan=0.0)

group_mean = np.nanmean(grades_matrix)
highest_grade = np.nanmax(grades_matrix)
lowest_grade = np.nanmin(grades_matrix)

low_grades_count = np.sum(
    (grades_matrix >= 1) & (grades_matrix <= 3), axis=1
)
students_need_attention = np.sum(student_means_safe < 7)

print(f"\n--- Крок 3: Результати аналізу ---")
print(f"Середній бал групи: {group_mean:.2f}")
print(f"Найвища оцінка: {highest_grade}, Найнижча оцінка: {lowest_grade}")
print(f"Студентів із середнім балом < 7 (Потребують уваги): {students_need_attention}")

statuses = [
    "Потребує уваги" if mean < 7 else "Добре" for mean in student_means_safe
]
results_df = pd.DataFrame(
    {
        "Студент": student_names,
        "Середній бал": np.round(student_means_safe, 2),
        "Оцінок 1–3": low_grades_count,
        "Статус": statuses,
    }
)
results_df.to_csv("results.csv", index=False, encoding="utf-8-sig")
print("Підсумкову таблицю збережено у results.csv")

# Крок 4. Візуалізація (Matplotlib)
# Графік 1: Середній бал студентів
plt.figure(figsize=(14, 6))
colors = ["red" if m < 7 else "skyblue" for m in student_means_safe]
plt.bar(
    range(len(student_names)), student_means_safe, color=colors, edgecolor="grey"
)
plt.axhline(y=7, color="orange", linestyle="--", label="Поріг (7 балів)")
plt.xticks(
    range(len(student_names)),
    [name.split()[0] for name in student_names],
    rotation=90,
    fontsize=9,
)
plt.xlabel("Студенти")
plt.ylabel("Середній бал")
plt.title("Середній бал студентів")
plt.legend()
plt.tight_layout()
plt.savefig("average_grades.png")
plt.close()

# Графік 2: Динаміка групи за датами
date_means = np.nanmean(grades_matrix, axis=0)
plt.figure(figsize=(12, 5))
plt.plot(
    date_column_names,
    date_means,
    marker="o",
    color="b",
    linestyle="-",
    linewidth=2,
)
plt.grid(True, linestyle=":", alpha=0.7)
plt.xlabel("Дата заняття")
plt.ylabel("Середній бал групи")
plt.title("Динаміка успішності групи за датами")
plt.xticks(rotation=45, fontsize=9)
plt.tight_layout()
plt.savefig("performance_trend.png")
plt.close()

# Графік 3: Розподіл оцінок
flat_grades = grades_matrix[~np.isnan(grades_matrix)]
plt.figure(figsize=(8, 5))
if len(flat_grades) > 0:
    n, bins, patches = plt.hist(
        flat_grades,
        bins=np.arange(0.5, 12.5, 1),
        edgecolor="black",
        color="skyblue",
    )
    for i in range(min(3, len(patches))):
        patches[i].set_facecolor("red")
plt.xlabel("Оцінки")
plt.ylabel("Кількість")
plt.title("Розподіл оцінок у журналі")
plt.xticks(range(1, 12))
plt.tight_layout()
plt.savefig("grades_distribution.png")
plt.close()
print("Усі три графіки (.png) успішно збережено!")

# Крок 5. Власний алгоритм сортування (Selection Sort) та лінійний пошук
def selection_sort_students(data_list):
    n = len(data_list)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if data_list[j]["Середній бал"] < data_list[min_idx]["Середній бал"]:
                min_idx = j
        data_list[i], data_list[min_idx] = data_list[min_idx], data_list[i]
    return data_list


students_list = results_df.to_dict(orient="records")
sorted_students = selection_sort_students(students_list.copy())

print("\n--- Крок 5: 5 найнижших результатів (Selection Sort) ---")
for student in sorted_students[:5]:
    print(
        f"{student['Студент']} — Середній бал: {student['Середній бал']} ({student['Статус']})"
    )


# Лінійний пошук студента
def linear_search_student(student_list, query_name):
    for student in student_list:
        if query_name.lower() in student["Студент"].lower():
            return student
    return None


# Приклад пошуку першого студента
query = student_names[0]
found = linear_search_student(students_list, query)
if found:
    print(f"\n[Лінійний пошук] Знайдено: {found['Студент']}")
    print(
        f"  - Середній бал: {found['Середній бал']}\n  - Статус: {found['Статус']}\n  - Оцінок 1-3: {found['Оцінок 1–3']}"
    )