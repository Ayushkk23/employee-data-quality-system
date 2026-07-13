import pandas as pd

def generate_summary_report(employees):
    if not isinstance(employees, pd.DataFrame):
        return "Invalid dataset."

    report = []
    report.append("Employee Data Quality Summary")
    report.append(f"Rows: {len(employees)}")
    report.append(f"Columns: {len(employees.columns)}")
    report.append("")
    report.append("Missing values per column:")
    report.append(employees.isna().sum().to_string())
    return "\n".join(report)