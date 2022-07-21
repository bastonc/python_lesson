from helpers.person import Person
from helpers.permissions import StudentPermission
from helpers.db_handler import db_handler


class Student(Person, StudentPermission):

    def __init__(self, program_lang, first_name, last_name, age, group, message='', db='lms.db'):
        super().__init__(first_name=first_name, last_name=last_name, age=age)
        self.last_name = last_name
        self.program_lang = program_lang
        self.group = group
        self.message = message
        self.db = db
        self.student_info = self.initialization_student()
        if not self.student_info:
            print("create student")
            self._create_student()
        self.student_id = self.student_info[0][0]

    def initialization_student(self):
        query = f'SELECT * FROM students WHERE `first_name`="{self.first_name}" AND `last_name`="{self.last_name}" AND `age`="{self.age}" AND `group_name`="{self.group}"'
        return db_handler(db=self.db, query=query)

    def get_group(self):
        return self.group

    def get_id(self):
        return self.student_id

    def _create_student(self):
        query = f'INSERT INTO students (`first_name`, `last_name`, `age`, `group_name`, `language`) \
        VALUES ("{self.first_name}", "{self.last_name}", {self.age}, "{self.group}", "{self.program_lang}")'
        db_handler(db=self.db, query=query)
        self.initialization_student()

    def __str__(self):
        return f'{self.message} Teacher {self.name} age: {self.age} - programm laguage {self.program_lang}, group(s) {[group for group in self.group]}'
