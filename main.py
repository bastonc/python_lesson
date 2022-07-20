from helpers.student import Student
from helpers.teacher import Teacher


if __name__ == '__main__':
    student1 = Student('Python', 'Sergey', 'Baston', 37, 'py_1', 'Group: py_1 Student')
    teacher = Teacher('Python', 'Bill', 'Gates', 67, group='py_1', message='Group: py_1 Teacher')
    student1.readiness_homework(8)
    teacher.check_homework(student1.get_id(), 8, 100)
