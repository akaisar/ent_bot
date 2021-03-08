from config import Config
from data.models import Student, MyEncoder
import requests
import json
import logging


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
    quiz_ids_for_user = {}

    def get_quiz_id_for_user(self, telegram_id):
        return self.quiz_ids_for_user[telegram_id][len(self.quizzes_for_user[telegram_id])]

    def set_quiz_ids_for_user(self, quiz_ids, telegram_id):
        self.quiz_ids_for_user[telegram_id] = quiz_ids

    def user_start_new_quiz(self, telegram_id):
        self.quizzes_for_user[telegram_id] = []
        self.quiz_ids_for_user[telegram_id] = []

    def user_make_answer_for_quiz(self, telegram_id, is_option_correct, number):
        self.quizzes_for_user[telegram_id].append(is_option_correct)
        logging.info(f"User: {telegram_id}, answer on {len(self.quizzes_for_user[telegram_id])}")
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
                    selected_language=c["selected_language"]
                )
            )

    def set_user_language(self, telegram_id, selected_language):
        for student in self.students:
            if student.telegram_id == telegram_id:
                student.selected_language = selected_language

    def get_user_language(self, telegram_id):
        for student in self.students:
            if student.telegram_id == telegram_id:
                return student.selected_language
        return "Русский"

    def post_user(self, telegram_id):
        for student in self.students:
            if student.telegram_id == telegram_id:
                return
        self.students.append(Student(
            telegram_id=telegram_id,
            selected_language="Русский",
            completed_quizzes=[]
        ))
        write_users_to_file("data_users.txt", self.students)

    def complete_quiz(self, telegram_id, quiz_id):
        for student in self.students:
            if student.telegram_id == telegram_id:
                if quiz_id not in student.completed_quizzes:
                    student.completed_quizzes.append(quiz_id)
