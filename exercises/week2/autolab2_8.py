
class Student: 
    def __init__(self, name, courses):
        self.name = name
        self.courses = courses

    def attends(self, course):
        return course in self.courses

def coursestudents(students: list, course: str):
    attending_students = []
    for student in students:
        if student.attends(course):
            attending_students.append(student.name)
    return attending_students

students = [Student('A', ['01005']), Student('B', ['02613']), Student('C', ['01005', '02613'])]
print(coursestudents(students,"02613"))