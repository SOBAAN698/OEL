class Student:
    def __init__(self, student_id=None, name="", student_class="", age=0):
        self.id = student_id
        self.name = name
        self.student_class = student_class
        self.age = age

    def __repr__(self):
        return f"Student(id={self.id}, name='{self.name}', class='{self.student_class}', age={self.age})"
