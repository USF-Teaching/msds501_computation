class Human():
    def __init__(self, name, age):
        self.name=name
        self.age=age

    def introduce(self):
        print(f'Hi I am {self.name}')

class Student(Human):
    def __init__(self, name, age, school):
        super().__init__(name,age)
        self.school=school
    def introduce(self):
        print(f"Hi, I'm {self.name} and I study at {self.school}.")

Prash=Student('Prashasti', 32, 'USFCA')
Prash.introduce()