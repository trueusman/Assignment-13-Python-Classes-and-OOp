"""Task 11: Merge student and score CSV files into a ranked gradebook."""

import csv

def grade_for(average):
    if average >= 85: return "A"
    if average >= 70: return "B"
    if average >= 55: return "C"
    if average >= 40: return "D"
    return "F"

def build_gradebook(students_path, scores_path, report_path="report.csv"):
    students = {}
    with open(students_path, newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            student_id = row["student_id"].strip()
            if student_id in students:
                raise ValueError(f"Duplicate student ID: {student_id}")
            students[student_id] = {"name": row["name"], "marks": []}

    seen = set()
    with open(scores_path, newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            student_id = row["student_id"].strip()
            subject = row["subject"].strip()
            if student_id not in students:
                raise ValueError(f"Unknown student ID: {student_id}")
            key = (student_id, subject)
            if key in seen:
                raise ValueError(f"Duplicate score for {student_id}/{subject}")
            seen.add(key)
            marks = float(row["marks"])
            if not 0 <= marks <= 100:
                raise ValueError("Marks must be between 0 and 100")
            students[student_id]["marks"].append(marks)

    report = []
    for student_id, data in students.items():
        marks = data["marks"]
        average = sum(marks) / len(marks) if marks else 0.0
        report.append({
            "student_id": student_id,
            "name": data["name"],
            "average": round(average, 2),
            "grade": grade_for(average)
        })

    report.sort(key=lambda row: (-row["average"], row["student_id"]))
    for rank, row in enumerate(report, 1):
        row["rank"] = rank

    with open(report_path, "w", newline="", encoding="utf-8") as file:
        fields = ["student_id", "name", "average", "grade", "rank"]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(report)
    return report


if __name__ == "__main__":
    with open("students.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["student_id", "name"])
        w.writerow(["101", "Ali"]); w.writerow(["102", "Sara"])
    with open("scores.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["student_id", "subject", "marks"])
        w.writerows([["101", "Python", 90], ["101", "SQL", 80],
                     ["101", "Math", 85], ["102", "Python", 92]])
    print(build_gradebook("students.csv", "scores.csv"))
