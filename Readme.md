# Employee Data Quality System

This project validates, cleans, analyzes, and reports on employee data using Python and Streamlit.

## Features

- CSV upload
- Column normalization and alias handling
- Data validation
- Missing value handling
- Duplicate removal
- Data analysis
- Cleaned CSV export
- Streamlit dashboard UI

## Project Structure

```text
employee-data-quality-system
├── src
│   ├── main.py
│   ├── validator.py
│   ├── cleaner.py
│   ├── Analyzer.py
│   └── reporter.py
├── reports
│   └── cleaned_employees.csv
├── requirements.txt
└── Readme.md
```

## Requirements

- Python 3.10+
- Streamlit
- Pandas

## Install Dependencies

```powershell
py -m pip install -r requirements.txt
```

If `requirements.txt` is missing Streamlit and Pandas:

```powershell
py -m pip install streamlit pandas
```

## Run the App

From the `src` folder:

```powershell
cd d:\employee-data-quality-system\src
streamlit run main.py
```

## Expected Dataset Columns

Required columns:

- `employee_id`
- `name`
- `age`
- `city`
- `department`
- `salary`

Optional columns are allowed, such as:

- `joining_date`

The app also supports aliases like:

- `employeeid` → `employee_id`
- `joiningdate` → `joining_date`

## Output

- Cleaned dataset saved in `reports/cleaned_employees.csv`
- Summary report displayed in the Streamlit UI
- Analysis metrics shown in the dashboard



## Notes

- Ensure all Python files import required modules correctly.
- Make sure the uploaded CSV contains the expected schema or supported aliases.
- The Streamlit app should be started from `src/main.py`.
