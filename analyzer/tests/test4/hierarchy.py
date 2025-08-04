class Animal:
    def eat(self):
        print("Animal is eating.")

class Mammal(Animal):
    def walk(self):
        print("Mammal is walking.")

class Human(Mammal):
    def speak(self):
        print("Human is speaking.")

h = Human()
h.eat()
h.walk()
h.speak()
