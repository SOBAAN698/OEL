class Teacher:
    def __init__(self, teacher_id=None, name="", subject=""):
        self.id = teacher_id
        self.name = name
        self.subject = subject

    def __repr__(self):
        return f"Teacher(id={self.id}, name='{self.name}', subject='{self.subject}')"
