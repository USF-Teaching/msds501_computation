class Human:
    def __init__(self, name, _age, __wage):
        self.name=name
        self._age=_age
        self.__wage=__wage

    def introduction(self):
        print(f"Hi I am {self.name}, my age is {self._age} and my wage is {self.__wage}")
    
prashasti= Human("Prashasti",32,0)
prashasti.introduction()
print(prashasti.name)     # Shubham
print(prashasti._age)     # 34 — works, but a signal not to
#print(prashasti.__wage)   # AttributeError
    
