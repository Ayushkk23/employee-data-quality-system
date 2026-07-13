import streamlit as st
import pandas as pd
from validator import (validate_columns, validate_missing_values, validate_salary, validate_duplicate_employee_ids)
from cleaner import (fill_missing_city, fill_missing_salary, fill_missing_age, remove_duplicate_rows, strip_extra_spaces, convert_datatypes)
from Analyzer import (average_salary, highest_salary, lowest_salary, employees_per_city, employees_per_department, salary_by_department)
from reporter import generate_summary_report

st.title("Employee Data Quality System")

uploaded_file = st.file_uploader("Upload Employee Dataset", type=["csv"])

if uploaded_file is not None:
    employees = pd.read_csv(uploaded_file)
    
    if employees.empty:
        st.error("Dataset is empty.")
    else:
        st.success("Employee Dataset Loaded Successfully")
        
        # Validate the dataset
        try:
            validate_columns(employees)
            validate_missing_values(employees)
            validate_salary(employees)
            validate_duplicate_employee_ids(employees)
            st.success("Validation completed successfully.")
        except Exception as e:
            st.error(f"Validation error: {e}")

        # Cleaning options
        if st.button("Clean Data"):
            employees = fill_missing_city(employees)
            employees = fill_missing_salary(employees)
            employees = fill_missing_age(employees)
            employees = remove_duplicate_rows(employees)
            employees = strip_extra_spaces(employees)
            employees = convert_datatypes(employees)
            st.success("Data cleaning completed successfully.")

            # Display cleaned data
            st.write("Cleaned Employee Dataset:")
            st.dataframe(employees)

            # Analysis
            st.subheader("Analysis Results")
            st.write(f"Average Salary: {average_salary(employees)}")
            st.write(f"Highest Salary: {highest_salary(employees)}")
            st.write(f"Lowest Salary: {lowest_salary(employees)}")
            st.write("Employees per City:")
            st.bar_chart(employees_per_city(employees))
            st.write("Employees per Department:")
            st.bar_chart(employees_per_department(employees))
            st.write("Salary by Department:")
            st.bar_chart(salary_by_department(employees))

            # Generate summary report
            if st.button("Generate Summary Report"):
                report = generate_summary_report(employees)
                st.success("Summary report generated.")
                st.write(report)

            # Save cleaned dataset
            if st.button("Save Cleaned Dataset"):
                employees.to_csv("reports/cleaned_employees.csv", index=False)
                st.success("Cleaned dataset saved successfully.")
else:
    st.info("Please upload a CSV file to get started.")