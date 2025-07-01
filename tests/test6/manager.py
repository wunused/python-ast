import person
from employee import Employee

class Manager(person.Person, Employee):
    def __init__(self, name, age, employee_id, department, team_size):
        person.Person.__init__(self, name, age)
        Employee.__init__(self, employee_id, department)
        self.team_size = team_size

    def display_manager_info(self):
        self.display_person_info()
        self.display_employee_info()
        print("Team Size:", self.team_size)

m = Manager("N", 35, 1, "D", 1)
