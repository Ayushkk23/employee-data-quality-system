from pathlib import Path
import re

import pandas as pd
import streamlit as st

from validator import (
    validate_columns,
    validate_missing_values,
    validate_salary,
    validate_duplicate_employee_ids,
)
from cleaner import (
    fill_missing_city,
    fill_missing_salary,
    fill_missing_age,
    remove_duplicate_rows,
    strip_extra_spaces,
    convert_datatypes,
)
from Analyzer import (
    average_salary,
    highest_salary,
    lowest_salary,
    employees_per_city,
    employees_per_department,
    salary_by_department,
)
from reporter import generate_summary_report

st.set_page_config(
    page_title="Employee Data Quality System",
    page_icon="📊",
    layout="wide",
)

st.title("Employee Data Quality System")
st.caption("Upload, validate, clean, analyze, and export employee data.")

EXPECTED_COLUMNS = [
    "employee_id",
    "name",
    "age",
    "city",
    "department",
    "salary",
]

COLUMN_ALIASES = {
    "employeeid": "employee_id",
    "employee id": "employee_id",
    "joiningdate": "joining_date",
    "joining date": "joining_date",
}

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [
        re.sub(r"[^a-z0-9]+", "_", str(col).strip().lower()).strip("_")
        for col in df.columns
    ]
    return df

def apply_column_aliases(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.rename(columns={c: COLUMN_ALIASES.get(c, c) for c in df.columns})
    return df

with st.sidebar:
    st.header("Upload")
    uploaded_file = st.file_uploader("Upload Employee Dataset", type=["csv"])
    st.markdown("---")
    st.markdown("**Expected columns**")
    st.code(", ".join(EXPECTED_COLUMNS))

if uploaded_file is None:
    st.info("Upload a CSV file to begin.")
    st.stop()

try:
    employees = pd.read_csv(uploaded_file)
except Exception as e:
    st.error(f"Could not read the CSV file: {e}")
    st.stop()

if employees.empty:
    st.error("Dataset is empty.")
    st.stop()

employees = normalize_columns(employees)
employees = apply_column_aliases(employees)

employees = strip_extra_spaces(employees)
employees = fill_missing_city(employees)
employees = fill_missing_salary(employees)
employees = fill_missing_age(employees)
employees = remove_duplicate_rows(employees)
employees = convert_datatypes(employees)

st.success("Employee dataset loaded successfully.")

with st.expander("View column names"):
    st.write(list(employees.columns))

missing_required = [col for col in EXPECTED_COLUMNS if col not in employees.columns]
if missing_required:
    st.error(f"Missing required columns: {', '.join(missing_required)}")
    st.stop()

extra_columns = [col for col in employees.columns if col not in EXPECTED_COLUMNS]
if extra_columns:
    st.warning(f"Extra columns detected: {', '.join(extra_columns)}")

try:
    validate_columns(employees)
    validate_missing_values(employees[EXPECTED_COLUMNS])
    validate_salary(employees)
    validate_duplicate_employee_ids(employees)

    st.success("Validation passed.")

    avg_salary = average_salary(employees)
    highest_sal = highest_salary(employees)
    lowest_sal = lowest_salary(employees)
    emp_per_city = employees_per_city(employees)
    emp_per_dept = employees_per_department(employees)
    salary_dept = salary_by_department(employees)
    report = generate_summary_report(employees)

    st.subheader("Analysis Results")
    m1, m2, m3 = st.columns(3)
    m1.metric("Average Salary", avg_salary)
    m2.metric("Highest Salary", highest_sal)
    m3.metric("Lowest Salary", lowest_sal)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["By City", "By Department", "Salary by Department", "Cleaned Data"]
    )

    with tab1:
        st.write(emp_per_city)

    with tab2:
        st.write(emp_per_dept)

    with tab3:
        st.write(salary_dept)

    with tab4:
        st.dataframe(employees, width="stretch")

    with st.expander("Summary Report"):
        st.write(report)

    reports_dir = Path("reports")
    reports_dir.mkdir(parents=True, exist_ok=True)

    cleaned_file_path = reports_dir / "cleaned_employees.csv"
    employees.to_csv(cleaned_file_path, index=False)

    st.success(f"Cleaned dataset saved to: {cleaned_file_path.as_posix()}")

    st.download_button(
        label="Download Cleaned CSV",
        data=employees.to_csv(index=False).encode("utf-8"),
        file_name="cleaned_employees.csv",
        mime="text/csv",
    )

except Exception as e:
    st.error(f"An error occurred: {e}")