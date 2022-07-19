from helpers.db_handler import db_handler


class TeacherPermission:

    def check_homework(self, student_id: int, hw_id: int, grade: int) -> None:
        query = f'UPDATE homeworks SET student_id={student_id}, grade={grade} WHERE hw_id={hw_id}'
        db_handler(db=self.db, query=query)


class StudentPermission:
    def __init__(self, student_id):
        self.student_id = student_id

    def readiness_homework(self, hw_id: int) -> None:
        print(self.student_info)
        query = f'INSERT INTO homeworks(student_id, hw_id, grade, readiness) VALUES({self.student_id}, {hw_id}, 0, True)'
        db_handler(db=self.db, query=query)

