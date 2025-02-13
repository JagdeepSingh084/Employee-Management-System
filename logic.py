import re
import os
import pandas as pd
import numpy as np

from data import EmployeeData

class Employee_services:
    def __init__(self, data_access):
        self.data_access = data_access

    #method to add employee
    def add_employee(self, id, name, salary, age, position):
        #validations
        try:
            if not id.isdigit() or int(id)<0:
                return "Employee id must be a positive integer"
            
            id = int(id)
        
            if not re.match(r"^[A-Za-z\s]+$", name):
                return "employee name must be a alphabet or space"

            #checking the employee id already exists in database
            if id in self.data_access.get_data()['ID'].values:
                return f"Employee with ID: {id} already exists in the database"

            #validating employee salary input
            try:
                salary = float(salary) if salary.strip() else np.nan  #if salary field is not empty
                if salary<0:
                    return "Salary must be a positive number"
            except ValueError as e:
                return "Invalid salary input"
            
            #validating employee age
            try:
                if age is None or age.strip() =="":
                    age = None
                elif age.isdigit():
                    age = int(age)
                else:
                    return "Age must be a positive integer value"
 
            except ValueError:
                return "Invalid age input"
            
            if position.strip():
                if not re.match(r"^[A-Za-z\s]+$", position):
                    return "Employee position can only contain alphabetic characters and spaces" 
            else:
                position = None
        except Exception as e:
            return "str(e)"
        
        #Calling add_employee 
        self.data_access.add_employee(id, name, salary, age, position)
        return None
    
    #method to delete employee by id
    def delete_employee_id(self, emp_id):
        if not emp_id.isdigit() or int(emp_id)<0:
            return "Employee id must be a positive integer"
            
        id = int(emp_id)

        if id not in self.data_access.get_data()['ID'].astype(int).values:
            return f"Employee with ID: {id} not found in the database"

        try:    
            msg = self.data_access.delete_employee_by_id(emp_id)
        except Exception as e:
            msg = f"{str(e)}"
        
        msg = "Employee deleted successfully!!"
    
    #Method to delete employee by name
    def delete_employee_name(self, emp_name):
        if not re.match(r"^[A-Za-z\s]+$", emp_name):
            return "Employee name must be a alphabet or space"
        
        if emp_name not in self.data_access.get_data()['Name'].astype(str).values:
            return f"Employee with name: {emp_name} not found in the database"
         
        try:
            msg = self.data_access.delete_employee_by_name(emp_name)
        
        except Exception as e:
            msg = f"{str(e)}"

        msg = "employee deleted successfully!!!"

    #method to update employee details by id
    def update_by_id(self, id, new_id, new_name, new_salary, new_age, new_position):
        try:
            #validating old ID
            if not id.isdigit():
                return "Employee ID must be a positive integer"
            id = int(id)
            
        except ValueError:
            return "Employee ID must be an integer"

        df = self.data_access.get_data()
        df['ID'] = df['ID'].astype(int)

        #find the employee id present in the datbase
        if id not in df['ID'].values:
            return f"Employee with ID: {id} not present in the database"
            
        #validating new ID
        if new_id.strip():
            try: 
                if not new_id.isdigit():
                    return "Employee ID must be a positive integer"
                new_id = int(new_id)

            except ValueError:
                return "Employee ID must be an integer"

        #checking if new_id is not already assigned to the employee in database
        if new_id != id and new_id in df['ID'].values:
            return f"Employee with ID: {new_id} already exists in the database"

        if new_name.strip() and not re.match(r"^[A-Za-z\s]+$", new_name):
            return "Employee name can only contain alphabetic characters and spaces"

        #salary validation
        if new_salary.strip():
            try:
                new_salary = float(new_salary)
            except ValueError:
                return "Salary must be a positive number"
            if new_salary<=0:
                return "Salary must be a positive number"
        
        if str(new_age).strip():
            try:
                new_age = int(new_age)
            except ValueError:
                return "Age must be a positive integer"
                
            if new_position.strip() and not re.match(r"^[A-Za-z\s]+$", new_position):
                return "Employee position can only contain alphabetic characters and spaces"
            
        #storing the original details of the employee
        emp_record = df.loc[df['ID'] == id].iloc[0]

        #updating new_details if new_details are provided
        new_id = new_id if new_id else emp_record['ID']
        new_name = new_name if new_name.strip() else emp_record['Name']
        new_salary = float(new_salary) if str(new_salary).strip() else emp_record['Salary']
        new_age = int(new_age) if str(new_age).strip() else emp_record['Age']
        new_position = new_position.strip() if new_position.strip() else emp_record['Position']

        # Convert Pandas int64 to native Python int before passing to MySQL
        new_id = int(new_id)
        new_salary = float(new_salary) if new_salary else np.nan
        new_age = pd.NA if str(new_age).strip() == "" else new_age

        try:
            self.data_access.update_employee_by_id(id, new_id, new_name, new_salary, new_age, new_position)
        except Exception as e:
            return f"Error occurred while updating employee details: {str(e)}"

    #Method to update employee details by using name
    def update_by_name(self, name, new_name, new_id, new_salary, new_age, new_position):
        try:
            if not name or not re.match(r"^[A-Za-z\s]+$", name.strip()):
                return "Employee name can only contain alphabetic characters and spaces"
            
            df = self.data_access.get_data()
            df['Name'] = df['Name'].astype(str)
            
            #find employee with the given name
            if str(name).lower() not in df['Name'].str.lower().values:
                return f"Employee with name: {name} not found in the database"
           
           #Validating new name
            if new_name and not re.match(r"^[A-Za-z\s]+$", new_name.strip()):
                return "Employee name can only contain alphabetic characters and spaces"
            
            #checking existance of new name inside the database
            if str(new_name).lower() != name.lower() and new_name.lower() in df['Name'].astype(str).str.lower().values:
                return f"Employee Name: {new_name} already exists"
            
            if new_salary.strip():
                try:
                    new_salary = float(new_salary)
                    if new_salary<=0:
                        return "Salary must be a positive number"
                except ValueError:
                    return "Invalid salary input"

            if new_age.strip():
                try:
                    new_age = int(new_age)
                except ValueError:
                    return "Employee age must be in digit"
            
            if new_position.strip() and not re.match(r"^[A-Za-z\s]+$", new_position):
                return "Employee position can only contain alphabetic characters and spaces"
            
            #storing the original details of the employee
            emp_record = df.loc[df['Name'].str.lower() == str(name).lower()].iloc[0]

            #updating new_details if new_details are provided
            new_id = int(new_id) if new_id.strip() else emp_record['ID']
            new_name = new_name.strip() if new_name.strip() else emp_record['Name']
            new_salary = float(new_salary) if str(new_salary).strip() else emp_record['Salary']
            new_age = int(new_age) if str(new_age).strip() else emp_record['Age']
            new_position = new_position.strip() if new_position.strip() else emp_record['Position']
            
            # Convert Pandas int64 to native Python int before passing to MySQL
            new_id = int(new_id)
            new_salary = float(new_salary) if new_salary else np.nan
            new_age = None if new_age is None else int(new_age)
    
            self.data_access.update_employee_by_name(name, new_name, new_id, new_salary, new_age, new_position)

        except Exception as e:
            return f"An error occurred: {str(e)}"
        

    #Method to display all the data
    def display_employee(self):
        try:
            return self.data_access.get_data()
        except (FileNotFoundError):
            return "Database not found. Please check the file if exist"
        except(pd.errors.EmptyDataError):
            return "No records found in the database"
        


    def conn_close(self):
        self.data_access.connection_close()