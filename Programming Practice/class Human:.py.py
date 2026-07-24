class Human:
    def __init__(self, name, age, wage):
        self.name = name
        self._age = age
        self.__wage = wage

obj = Human("Shubham", 34, 95000)
print(obj.name)     # Shubham
print(obj._age)     # 34 — works, but a signal not to
#print(obj.__wage)   # AttributeError
