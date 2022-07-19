from helpers.permissions import TeacherPermission
from helpers.person import Person


class Teacher(Person, TeacherPermission):

    def __init__(self, program_lang, first_name, last_name, age, group=None, message='', db='students.db'):
        super().__init__(first_name=first_name, last_name=last_name, age=age)
        self.program_lang = program_lang
        self.message = message
        self.db = db
        self.group = []
        if group:
            self.group.append(group)

    def add_group(self, group):
        self.group.append(group)

    def lead_group(self, group):
        if group in self.group:
            return True
        return False

    def __str__(self):
        return f'Teacher {self.name} age: {self.age} - programm laguage {self.program_lang}, group(s) {[group for group in self.group]}'
