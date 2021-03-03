from config import Config
from data.models import Student, MyEncoder
import requests
import json


def read_user_from_file(file_name):
    with open(file_name, "rb") as f:
        return f.read()


def write_users_to_file(file_name, users):
    with open(file_name, "w") as f:
        f.write(json.dumps(users, cls=MyEncoder))


class UserService:
    users = []
    students = []
    quizzes_for_user = {}

    def user_start_new_quiz(self, telegram_id):
        self.quizzes_for_user[telegram_id] = []

    def user_make_answer_for_quiz(self, telegram_id, is_option_correct, number):
        self.quizzes_for_user[telegram_id].append(is_option_correct)
        if len(self.quizzes_for_user[telegram_id]) == number:
            correct_answer_number = 0
            for option in self.quizzes_for_user[telegram_id]:
                if option:
                    correct_answer_number += 1
            return [True, correct_answer_number]
        else:
            return [False]

    def get_users(self):
        data = read_user_from_file("data_users.txt")
        for c in json.loads(data):
            self.students.append(
                Student(
                    telegram_id=c["telegram_id"],
                    completed_quizzes=c["completed_quizzes"],
                )
            )

    def post_user(self, telegram_id):
        for student in self.students:
            if student.telegram_id == telegram_id:
                return
        self.students.append(Student(
            telegram_id=telegram_id,
            completed_quizzes=[]
        ))
        write_users_to_file("data_users.txt", self.students)

    def complete_quiz(self, telegram_id, quiz_id):
        for student in self.students:
            if student.telegram_id == telegram_id:
                student.completed_quizzes.append(quiz_id)
