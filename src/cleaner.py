import pandas as pd

def _blank_to_na(df):
    df = df.copy()
    return df.replace(r"^\s*$", pd.NA, regex=True)

def fill_missing_city(employees):
    employees = _blank_to_na(employees)
    if "city" in employees.columns:
        employees["city"] = employees["city"].fillna("Unknown")
    return employees

def fill_missing_salary(employees):
    employees = _blank_to_na(employees)
    if "salary" in employees.columns:
        employees["salary"] = pd.to_numeric(employees["salary"], errors="coerce")
        employees["salary"] = employees["salary"].fillna(employees["salary"].median())
    return employees

def fill_missing_age(employees):
    employees = _blank_to_na(employees)
    if "age" in employees.columns:
        employees["age"] = pd.to_numeric(employees["age"], errors="coerce")
        employees["age"] = employees["age"].fillna(employees["age"].median())
        employees["age"] = employees["age"].round().astype("Int64")
    return employees

def remove_duplicate_rows(employees):
    employees = employees.copy()
    if "employee_id" in employees.columns:
        employees = employees.drop_duplicates(subset="employee_id", keep="first")
    else:
        employees = employees.drop_duplicates(keep="first")
    return employees

def strip_extra_spaces(employees):
    employees = employees.copy()
    for col in employees.select_dtypes(include=["object", "string"]).columns:
        employees[col] = employees[col].astype("string").str.strip()
    return employees

def convert_datatypes(employees):
    employees = employees.copy()

    if "employee_id" in employees.columns:
        employees["employee_id"] = pd.to_numeric(employees["employee_id"], errors="coerce")
        employees["employee_id"] = employees["employee_id"].round().astype("Int64")

    if "age" in employees.columns:
        employees["age"] = pd.to_numeric(employees["age"], errors="coerce")
        employees["age"] = employees["age"].round().astype("Int64")

    if "salary" in employees.columns:
        employees["salary"] = pd.to_numeric(employees["salary"], errors="coerce")

    return employees