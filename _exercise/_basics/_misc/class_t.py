
class Person:
    def __init__(self, fname, lname):
        self.firstname = fname
        self.lastname = lname

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class Student(Person):
    def __init__(self, fname, lname, year):
        super().__init__(fname, lname)
        self.graduationyear = year
    def __str__(self):
        return f"{self.firstname} {self.lastname} -- class of {self.graduationyear}"

x = Student("Mike", "Olsen", 2019)
print(x)
