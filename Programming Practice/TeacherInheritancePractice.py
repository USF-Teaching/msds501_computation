class Human():
    def __init__(self,name, age, wage):
        self.name=name
        self.age=age
        self.wage=wage
    def introduce(self):
        print(f'{self.name}')



class Teacher(Human):
    def __init__(self, name, age, wage, watewa):
        super().__init__(name, age, wage)
        self.watewa=watewa
    def introduce(self):
        print('override')

obj=Human('Prash',32,300,000)
