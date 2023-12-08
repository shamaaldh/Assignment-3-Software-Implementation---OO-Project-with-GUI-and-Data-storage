import pickle
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog

# Define the classes
class Employee:
    def __init__(self, name, id_number, department, job_title, basic_salary, age, dob, passport_details):
        self.name = name
        self.id_number = id_number
        self.department = department
        self.job_title = job_title
        self.basic_salary = basic_salary
        self.age = age
        self.date_of_birth = datetime.strptime(dob, '%d-%m-%Y')
        self.passport_details = passport_details
        self.sales = []

    def calculate_salary(self, month_year):
        monthly_commission = sum(sale.calculate_commission() for sale in self.sales if sale.date_of_sale.strftime('%m-%Y') == month_year)
        return self.basic_salary + monthly_commission

    def add_sale(self, sale):
        self.sales.append(sale)

    def __str__(self):
        return f'Employee: {self.name}, ID: {self.id_number}, Department: {self.department}, Title: {self.job_title}'

class Manager(Employee):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sales_team = []

    def calculate_commission(self, sale):
        return sale.calculate_profit() * 0.0325

    def add_salesperson(self, salesperson):
        self.sales_team.append(salesperson)
        salesperson.manager = self

class Salesperson(Employee):
    def calculate_commission(self, sale):
        return sale.calculate_profit() * 0.065

class House:
    def __init__(self, name, id_number, declared_price, house_type, built_up_area, status, number_of_rooms, number_of_bathrooms):
        self.name = name
        self.id_number = id_number
        self.declared_price = declared_price
        self.type = house_type
        self.built_up_area = built_up_area
        self.status = status
        self.selling_price = None
        self.number_of_rooms = number_of_rooms
        self.number_of_bathrooms = number_of_bathrooms

    def update_status(self, new_status, selling_price=None):
        self.status = new_status
        if selling_price:
            self.selling_price = selling_price

    def __str__(self):
        return f'House: {self.name}, ID: {self.id_number}, Type: {self.type}, Status: {self.status}'

class Sale:
    def __init__(self, house, salesperson, sale_price, date_of_sale):
        self.house = house
        self.salesperson = salesperson
        self.sale_price = sale_price
        self.date_of_sale = datetime.strptime(date_of_sale, '%d-%m-%Y')

    def calculate_profit(self):
        profit = self.sale_price - self.house.declared_price
        return profit if profit > 0 else 0

# Functions to handle file operations for persistence
def save_to_file(data, filename):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)

def load_from_file(filename):
    try:
        with open(filename, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return []

# GUI functions
def add_employee_gui():
    name = simpledialog.askstring("Input", "Enter employee's name")
    if not name:
        return
    id_number = simpledialog.askstring("Input", "Enter employee's ID number")
    department = simpledialog.askstring("Input", "Enter employee's department")
    job_title = simpledialog.askstring("Input", "Enter employee's job title")
    basic_salary = simpledialog.askinteger("Input", "Enter employee's basic salary")
    age = simpledialog.askinteger("Input", "Enter employee's age")
    dob = simpledialog.askstring("Input", "Enter employee's date of birth (dd-mm-yyyy)")
    passport_details = simpledialog.askstring("Input", "Enter employee's passport details")
    
    # Create the employee object
    if job_title == 'Manager':
        employee = Manager(name, id_number, department, job_title, basic_salary, age, dob, passport_details)
    else:
        employee = Salesperson(name, id_number, department, job_title, basic_salary, age, dob, passport_details)
    
    # Load existing employees, add the new one, save back to file
    employees = load_from_file('employees.pkl')
    employees.append(employee)
    save_to_file(employees, 'employees.pkl')
    messagebox.showinfo("Success", "Employee added successfully!")

def display_employees_gui():
    employees = load_from_file('employees.pkl')
    employee_details = "\n".join(str(employee) for employee in employees)
    messagebox.showinfo("Employees", employee_details)

# Main GUI Application
def main_app():
    root = tk.Tk()
    root.title("BrickCages Real Estate Management System")

    # Add Employee Button
    add_emp_button = tk.Button(root, text="Add Employee", command=add_employee_gui)
    add_emp_button.pack()

    # Display Employee Button
    disp_emp_button = tk.Button(root, text="Display Employees", command=display_employees_gui)
    disp_emp_button.pack()

    # Run the application
    root.mainloop()

if __name__ == "__main__":
    main_app()
