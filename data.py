import pandas as pd
import mysql.connector

#Using SQL conenctor to store the data into the database
class EmployeeData:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
        host=host,
        user=user,
        password= password,
        database= database
        )
        self.cursor = self.conn.cursor(dictionary = True)# Enables column names as keys
        try:
            query = """
                    CREATE TABLE IF NOT EXISTS employee_table(
                    ID INT PRIMARY KEY,
                    Name VARCHAR(225) NOT NULL,
                    Salary DECIMAL(10,2),
                    Age INT,
                    Position VARCHAR(225)
                    )"""
            self.cursor.execute(query)
            self.conn.commit()

        except mysql.connector.Error as e:
            print("database error: {str(e)}")

    #fetching all data from the table
    def get_data(self):
        self.cursor.execute("SELECT * FROM employee_table")
        data = self.cursor.fetchall() # Fetch data as list of dictionaries
        df = pd.DataFrame(data) if data else pd.DataFrame(columns=['ID', 'Name', 'Salary', 'Age', 'Position'])
    
       #conversion for nullable column values
        df['Salary']  = df['Salary'].astype(float)
        df['Age']  = df['Age'].astype('Int64')
        
        return df
    #add new employee to the database
    def add_employee(self, id, name, salary, age, position):
        try:
            age = int(age) if pd.notna(age) else None
            query = "INSERT INTO employee_table(ID, Name, Salary, Age, Position) VALUES(%s, %s, %s, %s, %s)"
            self.cursor.execute(query, (id, name, salary, age, position))
            self.conn.commit()
            return None
        except mysql.connector.Error as error:
            return str(error)
    
    #delete employee by id
    def delete_employee_by_id(self, emp_id):
        self.cursor.execute("DELETE FROM employee_table WHERE ID = %s", (emp_id,))
        self.conn.commit()
        return None

    #delete employee by name
    def delete_employee_by_name(self, emp_name):
       self.cursor.execute("DELETE FROM employee_table WHERE Name = %s", (emp_name,))
       self.conn.commit()
       return None

    #Updating employee by id
    def update_employee_by_id(self, id, new_id, new_name, new_salary, new_age, new_position):
        new_age = None if pd.isna(new_age) or str(new_age).strip() == "" else int(new_age)
        query = """
                UPDATE employee_table SET
                ID = %s,
                Name=%s,
                Salary=%s,
                Age=%s,
                Position=%s
                WHERE ID=%s
                """
        values = (new_id, new_name, new_salary, new_age, new_position, id)
        self.cursor.execute(query, values)
        self.conn.commit()
        return None

    #Updating employee by name
    def update_employee_by_name(self,name, new_name, new_id, new_salary, new_age, new_position):
        new_age = None if pd.isna(new_age) or str(new_age).strip() == "" else int(new_age)
        query = """
                UPDATE employee_table SET
                id = %s,
                Name=%s,
                Salary=%s,
                Age=%s,
                Position=%s
                WHERE Name=%s
                """
        values = (new_id,new_name, new_salary, new_age, new_position, name)
        self.cursor.execute(query, values)
        self.conn.commit()

    #closing the connection
    def connection_close(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.conn is not None:
            self.conn.close()
    