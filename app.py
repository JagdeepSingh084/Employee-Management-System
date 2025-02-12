#Employee data
import sys
import time
import streamlit as st 
from data import EmployeeData
from logic import Employee_services

#Title for employee
st.title('Employee Data')

#Initialize data layer and logic layer classes
data_access = EmployeeData( host="localhost",user="root",password= "Qwer@1234", database= "employee")
logic_layer = Employee_services(data_access)


st.subheader("Please select your choice")
st.write("--------------------------------")



#Initialize session state variables
if "show_inputs" not in st.session_state:
    st.session_state.show_inputs = False

if "action" not in st.session_state:
    st.session_state.action = None


#Add employee
Add_new_employee = st.button("Add new employee")
if Add_new_employee:
    st.session_state.show_inputs = True
    st.session_state.action = "add"

if st.session_state.show_inputs and st.session_state.action == "add":
    with st.form("Adding_employee"):
        emp_id = st.text_input("Enter the employee ID: ", value = "", placeholder = "101, 102, etc")
        emp_name = st.text_input("Enter the employee name: ")
        emp_salary = st.text_input("Enter the employee salary: ")
        emp_age = st.text_input("Enter the employee age: ")
        emp_position = st.text_input("Enter the employee position: ")
        #submit button to add employee after clicking the add employ
        submitted = st.form_submit_button("Submit")
        if submitted:
            if emp_id and emp_name:
            
                result = logic_layer.add_employee(emp_id, emp_name, emp_salary,emp_age, emp_position)
                if result is None:
                    st.success("Employee added successfully!!!")
                    #reset all input fields and hide submit button
                    st.session_state.show_inputs = False
                    st.session_state.action = None
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error(result)
            else:
                st.warning('Please enter Employee ID and Name')

#Button to Delete employee by ID
Delete_employee_by_ID = st.button("Delete employee by ID")
if Delete_employee_by_ID:
    st.session_state.show_inputs = True
    st.session_state.action = "delete"

if st.session_state.show_inputs and st.session_state.action == "delete":
    with st.form("Delete employee by id"):
        delete_emp_id = st.text_input("Enter the employee ID To be deleted: ")

        submitted = st.form_submit_button("Submit")
        if submitted:
            if delete_emp_id:
            #call delete by id method
                result = logic_layer.delete_employee_id(delete_emp_id)
                if result:
                    st.error(result)
                else:
                    st.success("Employee deleted successfully!!")
                    st.session_state.show_inputs = False
                    st.session_state.action = None
                    time.sleep(1)
                    st.rerun()
            else:
                st.warning('Please enter Employee ID')

#button to delete employee by Name
Delete_employee_by_Name = st.button("Delete employee by Name")
if Delete_employee_by_Name:
    st.session_state.show_inputs = True
    st.session_state.action = "delete_name"

if st.session_state.show_inputs and st.session_state.action == "delete_name":
    with st.form("Delete by name"):
        delete_emp_name = st.text_input("Enter the name of employee to be deleted")
       
        submit = st.form_submit_button("Submit")
        if submit:
            if delete_emp_name:
                result = logic_layer.delete_employee_name(delete_emp_name)
                if result:
                    st.error(result)
                else:
                    st.success("Employee details updated successfully!!")
                    st.session_state.show_inputs = False
                    st.session_state.action = None
                    time.sleep(1)
                    st.rerun()
                
            else:
                st.warning('Please enter Employee Name.')



# Button for Updating employee details by ID
Update_details_by_id = st.button("Update details by id")
if Update_details_by_id:
    st.session_state.show_inputs = True
    st.session_state.action = "update_id"

# Ensure input fields are displayed correctly
if st.session_state.show_inputs and st.session_state.action == "update_id":
    with st.form("update by id"):
           
        emp_id = st.text_input("Enter the employee ID: ", st.session_state.get("emp_id", ""))
        emp_new_id = st.text_input("Enter new id for the employee: ", st.session_state.get("emp_new_id", "" )) 
        emp_name = st.text_input("Enter new employee name: ", st.session_state.get("emp_name", ""))
        emp_salary = st.text_input("Enter new employee salary: ", st.session_state.get("emp_salary",""))
        emp_age = st.text_input("Enter new employee age: ", st.session_state.get("emp_age", ""))
        emp_position = st.text_input("Enter new employee position: ", st.session_state.get("emp_position", ""))

        submitted = st.form_submit_button("Submit")
        if submitted:
            if emp_id:
                result = logic_layer.update_by_id(emp_id, emp_new_id, emp_name, emp_salary, emp_age, emp_position)
                if result:
                    st.error(result)
                else:
            # Reset session state only after successful update
                    st.success("Employee details updated Successfully!!!")
                    st.session_state.show_inputs = False
                    st.session_state.action = None
                    time.sleep(1)
                    st.rerun()
            else:
                st.warning("Please the employee ID to be updated")

#button for updating Employee details by their name
Updating_details_by_name = st.button("Update details by name")
if Updating_details_by_name:
    st.session_state.show_inputs = True
    st.session_state.action = "update_name"

if st.session_state.show_inputs and st.session_state.action == "update_name":
    with st.form("update by name"):
        emp_name_to_update = st.text_input("Enter the employee name: ", st.session_state.get("emp_name_to_update", ""))
        emp_new_name = st.text_input("Enter new name for the employee: ", st.session_state.get("emp_new_name", ""))
        emp_id = st.text_input("Enter new employee ID: ", st.session_state.get("emp_id", ""))
        emp_salary = st.text_input("Enter new employee salary: ", st.session_state.get("emp_salary", ""))
        emp_age = st.text_input("Enter new employee age: ", st.session_state.get("emp_age", ""))
        emp_position = st.text_input("Enter new employee position: ", st.session_state.get("emp_position", ""))

        submitted = st.form_submit_button("submit")
        if submitted:
            if emp_name_to_update:
                result = logic_layer.update_by_name(emp_name_to_update, emp_new_name, emp_id, emp_salary, emp_age, emp_position)
                if result:
                    st.error(result)
                else:
                     #resetting the input fields visible
                    st.success("Employee details updated Successfully!!!") 
                    st.session_state.show_inputs = False
                    st.session_state.action = None
                    time.sleep(1)
                    st.rerun()
            else:
                st.warning("Please enter the employee name")

#Button to display all employee
show_all_employee = st.button("Show all employee")
if show_all_employee:
    employee = logic_layer.display_employee()
    if employee is not None:
        st.table(employee)
    else:
        st.write("No employee")


#Exit button to end the streamlit app
exit = st.button('Exit')

if exit:
    st.write("Exiting the app")
    result = logic_layer.conn_close()
    if result is not None:
        st.error(result)
        
    time.sleep(2)
    st.markdown("""
        <meta http-equiv="refresh" content="0; url='https://www.google.com'" />
        """, unsafe_allow_html=True
    )

