import pandas as pd

def average_salary(employees):
    return employees['salary'].mean()

def highest_salary(employees):
    return employees['salary'].max()

def lowest_salary(employees):
    return employees['salary'].min()

def employees_per_city(employees):
    return employees['city'].value_counts()

def employees_per_department(employees):
    return employees['department'].value_counts()

def salary_by_department(employees):
    return employees.groupby('department')['salary'].mean()