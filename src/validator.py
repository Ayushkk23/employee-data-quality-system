def validate_columns(employees):
    required_columns = ['employee_id', 'name', 'age', 'city', 'salary', 'department']
    for column in required_columns:
        if column not in employees.columns:
            raise ValueError(f"Missing required column: {column}")

def validate_missing_values(employees):
    if employees.isnull().sum().sum() > 0:
        raise ValueError("Dataset contains missing values.")

def validate_salary(employees):
    if not all(employees['salary'] >= 0):
        raise ValueError("Salary must be a non-negative value.")

def validate_duplicate_employee_ids(employees):
    if employees['employee_id'].duplicated().any():
        raise ValueError("Duplicate employee IDs found.")