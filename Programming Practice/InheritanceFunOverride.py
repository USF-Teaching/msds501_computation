class Human():
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def introduce(self):
        print(f'Baby {self.name}')

class Baby(Human):
    def __init__(self, name, age, month):
        super().__init__(name, age)
        self.month=month

    def introduce(self):
            print("Goo Goo Gaga")

    def print_sleep_hours(self):
            if self.month < 1:
                print("Sleep 16 hrs")
            elif self.month <=6:
                print('15 hrs')
            else:
                print('sleep 14 hrs')

b=Baby('Vatsu',1,12)
b.introduce()
b.print_sleep_hours()
