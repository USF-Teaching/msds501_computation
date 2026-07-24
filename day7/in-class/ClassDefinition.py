class Human:
    def __init__(self, name, age):
        self.name=name
        self.age=age
    
    def introduction(self):
        print(f"Hi, I'm {self.name}")

shubham =Human("Shubham",34)
shubham.introduction()