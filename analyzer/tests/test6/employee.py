class Employee:
    def __init__(self, employee_id, department):
        self.employee_id = employee_id
        self.department = department

    def display_employee_info(self):
        print("ID:", self.employee_id, "Department:", self.department)

e = Employee(100, "Marketing")
