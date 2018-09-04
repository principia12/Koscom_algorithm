class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.accepted_year = student_id[:4]
        
    def __str__(self):
        return ''%(self.student_id, self.name)
        
        