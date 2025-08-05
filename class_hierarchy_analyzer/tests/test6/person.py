class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def display_person_info(self):
        print("Name:", self.name, "Age:", self.age)

p = Person("Alyssa", 20)
