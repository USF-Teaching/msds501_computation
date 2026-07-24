class Human:
    def __init__(self, name, age, school):
        self.name = name
        self.age = age
        self.school = school

obj = Human("Shubham", 34, 'la')
print(obj.name)     # Shubham
print(obj.age)     # 34 — works, but a signal not to
print(obj.school)   # AttributeError


class Student(Human):
    def __init__(self, name, age, school):
        super().__init__(name, age)
        self.school = school

    def introduce(self):
        print(f"Hi, I'm {self.name} and I study at {self.school}.")

s = Student("Shubham", 34, "USF")
s.introduce()
# Hi, I'm Shubham and I study at USF.
