from config import Config
from data.models import Student, MyEncoder
import requests
import json
import logging


def read_users_from_api():
    r = requests.get(Config.API_URL+"userDb")
    data = json.loads(r.text)
    students = []
    for line in data:
        student = Student(telegram_id=line["telegram_id"], selected_language=line["selected_language"],
                          completed_quizzes=line["quizzes"])
        students.append(student)
    return students


async def post_user_to_api(user):
    json_user = {
        "telegram_id": user.telegram_id,
        "selected_language": user.selected_language,
        "quizzes": user.completed_quizzes
    }
    r = requests.post(Config.API_URL+"userDb", json_user)
    print(r)


async def put_args_to_api(args):
    r = requests.put(Config.API_URL+"userDb", json=args)
    print(r)


class UserService:
    users = []
    students = []
    quizzes_for_user = {}
    quiz_ids_for_user = {}

    def get_quiz_results(self, telegram_id):
        return self.quizzes_for_user[telegram_id]

    def get_quiz_ids_for_user(self, telegram_id):
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
        self.students = read_users_from_api()

    def set_user_language(self, telegram_id, selected_language):
        for student in self.students:
            if student.telegram_id == telegram_id:
                student.selected_language = selected_language
        await put_args_to_api({"telegram_id": telegram_id, "selected_language": selected_language})

    def get_user_language(self, telegram_id):
        for student in self.students:
            if student.telegram_id == telegram_id:
                return student.selected_language
        return "Русский"

    def post_user(self, telegram_id):
        for student in self.students:
            if student.telegram_id == telegram_id:
                return
        student = Student(
            telegram_id=telegram_id,
            selected_language="Русский",
            completed_quizzes=[]
        )
        self.students.append(student)
        await post_user_to_api(student)

    def complete_quiz(self, telegram_id, quiz_id):
        for student in self.students:
            if student.telegram_id == telegram_id:
                if quiz_id not in student.completed_quizzes:
                    student.completed_quizzes.append(quiz_id)
                    await put_args_to_api({"telegram_id": telegram_id, "quizzes": student.completed_quizzes})