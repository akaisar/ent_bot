import json
import logging

import requests_async as requests

from config import Config
from data.models import Student, Teacher, User, Tutor
from localization.localization import Localization as local, Data


def json_to_obj(json_obj, user_type):
    if user_type == Config.STUDENTS:
        return Student(telegram_id=json_obj["telegram_id"])
    elif user_type == Config.USERS:
        return User(telegram_id=json_obj["telegram_id"], selected_language=Config.LANGUAGE_DATA[
            json_obj["selected_language"]],
                    user_state=Config.USER_STATE_DATA[json_obj["user_state"]], name=json_obj["name"])
    elif user_type == Config.TEACHERS:
        return Teacher(telegram_id=json_obj["telegram_id"],
                       students=json_obj["students"], referral=json_obj["referral"])
    elif user_type == Config.TUTORS:
        return Tutor(telegram_id=json_obj["telegram_id"])
    else:
        logging.info("Incorrect user type")


# MARK: API interaction


async def get_users_from_api():
    logging.info("Start load users from api")
    users = {}
    for user_type in Config.USER_DB:
        logging.info(f"Start load {user_type}")
        r = await requests.get(Config.API_URL + user_type)
        data = json.loads(r.text)
        objects = {}
        for json_obj in data:
            objects[json_obj["telegram_id"]] = json_to_obj(json_obj, user_type)
        users[user_type] = objects
        logging.info(f"Finish load {user_type}")
    logging.info("Finish load users from api")
    return users


async def post_user_to_api(user, user_type):
    r = await requests.post(Config.API_URL + user_type, json=user.to_json())
    return json.loads(r.text)


async def put_args_to_api(user, user_type):
    r = await requests.put(Config.API_URL + user_type, json=user.to_json())


class UserService:
    users = {}

    quiz_results = {}
    quiz_type = {}
    quiz_ids = {}
    quiz_size = {}
    quiz_sets = {}
    quiz_set_index = {}

    def set_quiz_sets(self, telegram_id, quiz_sets):
        self.quiz_sets[telegram_id] = quiz_sets
        self.quiz_set_index[telegram_id] = 0

    def is_send_text(self, telegram_id):
        index = self.quiz_set_index[telegram_id]
        quiz_id = 0
        cnt = 0
        for quiz_set in self.quiz_sets[telegram_id]:
            for index2 in range(len(quiz_set.quizzes)):
                if cnt == index:
                    if index2 == 0:
                        self.quiz_set_index[telegram_id] = index + 1
                        return True
                    self.quiz_set_index[telegram_id] = index + 1
                    return False
                cnt += 1

    def set_quiz_type(self, telegram_id, type):
        self.quiz_type[telegram_id] = type

    def get_quiz_type(self, telegram_id):
        return self.quiz_type[telegram_id]

    def set_quiz_size(self, telegram_id, size):
        self.quiz_size[telegram_id] = size

    def get_quiz_size(self, telegram_id):
        return self.quiz_size[telegram_id]
    # MARK: User quiz interaction

    def get_quiz_ids_for_user(self, telegram_id):
        return self.quiz_ids[telegram_id][len(self.quiz_results[telegram_id])]

    def set_quiz_ids_for_user(self, quiz_ids, telegram_id):
        self.quiz_ids[telegram_id] = quiz_ids

    def get_quiz_results(self, telegram_id):
        return self.quiz_results[telegram_id]

    def user_start_new_quiz(self, telegram_id):
        self.quiz_results[telegram_id] = []
        self.quiz_ids[telegram_id] = []

    def user_make_answer_for_quiz(self, telegram_id, is_option_correct, number):
        self.quiz_results[telegram_id].append(is_option_correct)
        logging.info(f"User: {telegram_id}, answer on {len(self.quiz_results[telegram_id])}")
        if len(self.quiz_results[telegram_id]) == number:
            return True
        else:
            return False


    # MARK: Users

    async def post_user(self, telegram_id):
        if telegram_id not in self.users[Config.USERS]:
            for user_type in Config.USER_DB:
                json_obj = await post_user_to_api(user=Config.USER_TYPE_MODEL[user_type](telegram_id=telegram_id),
                                                  user_type=user_type)
                self.users[user_type][telegram_id] = json_to_obj(json_obj=json_obj, user_type=user_type)
            return True
        return False

    async def get_users(self):
        self.users = await get_users_from_api()

    def user_exists(self, telegram_id):
        return telegram_id in self.users[Config.USERS]

    # MARK: Language

    async def set_language(self, telegram_id, selected_language):
        self.users[Config.USERS][telegram_id].selected_language = selected_language
        await put_args_to_api(user=self.users[Config.USERS][telegram_id], user_type=Config.USERS)

    def get_language(self, telegram_id):
        return self.users[Config.USERS][telegram_id].selected_language

    # MARK: User state

    async def set_user_state(self, telegram_id, user_state):
        self.users[Config.USERS][telegram_id].user_state = user_state
        await put_args_to_api(user=self.users[Config.USERS][telegram_id], user_type=Config.USERS)

    def get_user_state(self, telegram_id):
        if telegram_id in self.users[Config.USERS]:
            return self.users[Config.USERS][telegram_id].user_state
        else:
            return ""

    def is_student(self, telegram_id):
        return self.get_user_state(telegram_id=telegram_id) == Data.STUDENT

    def is_teacher(self, telegram_id):
        return self.get_user_state(telegram_id=telegram_id) == Data.TEACHER

    def is_tutor(self, telegram_id):
        return self.get_user_state(telegram_id=telegram_id) == Data.TUTOR

    # MARK: User name

    async def set_user_name(self, telegram_id, name):
        self.users[Config.USERS][telegram_id].name = name
        await put_args_to_api(self.users[Config.USERS][telegram_id], Config.USERS)

    def get_name(self, telegram_id):
        return self.users[Config.USERS][telegram_id].name

    # MARK: Set student to teacher

    async def set_student_to_teacher(self, telegram_id, referral):
        data = self.find_teacher_by_referral(referral=referral)
        if data[0]:
            teacher = data[1]
            for student in teacher.students:
                if student == telegram_id:
                    return data[0]
            teacher.students.append(telegram_id)
            await put_args_to_api(teacher, Config.TEACHERS)
        return data[0]

    # MARK: Find student by referral

    def find_teacher_by_referral(self, referral):
        for telegram_id, teacher in self.users[Config.TEACHERS].items():
            if teacher.referral == referral:
                return [True, teacher]
        return [False]

    # MARK: Delete student from teacher

    async def delete_student_from_teacher(self, teacher_id, student_pos):
        student_pos = int(student_pos)
        if student_pos < len(self.users[Config.TEACHERS][teacher_id].students):
            student_id = self.users[Config.TEACHERS][teacher_id].students[student_pos]
            self.users[Config.TEACHERS][teacher_id].students.remove(student_id)
            await put_args_to_api(self.users[Config.TEACHERS][teacher_id], Config.TEACHERS)
            return True
        else:
            return False

    # MARK: Get teacher students

    def get_teacher_students(self, telegram_id):
        return self.users[Config.TEACHERS][telegram_id].students

    def get_teacher_referral(self, telegram_id):
        return self.users[Config.TEACHERS][telegram_id].referral

    # MARK: Get student subjects

    def get_student_subjects(self, telegram_id):
        return self.users[Config.STUDENTS][telegram_id].subject_1, self.users[Config.STUDENTS][telegram_id].subject_2

    # MARK: Set student subjects

    def set_student_subjects(self, telegram_id, subject_num, subject):
        if subject_num == 1:
            self.users[Config.STUDENTS][telegram_id].subject_1 = subject
        else:
            self.users[Config.STUDENTS][telegram_id].subject_2 = subject

    @staticmethod
    async def get_student_stats(telegram_id):
        r = await requests.get(Config.API_URL+Config.STUDENTS+"/"+str(telegram_id)+"/stats")
        logging.info("Get user stats: "+str(r))
        json_obj = json.loads(r.text)
        return json_obj

    # MARK: Get user profile
    def get_user_profile(self, telegram_id, user_language):
        name = self.get_name(telegram_id)
        language = self.get_language(telegram_id)
        user_state = self.get_user_state(telegram_id)
        subject_1, subject_2 = self.get_student_subjects(telegram_id)
        return f"{local.data[Data.USER_NAME_BUTTON][user_language]}: {name}\n" \
               f"{local.data[Data.LANGUAGE_BUTTON][user_language]}: {local.data[language][user_language]}\n" \
               f"{local.data[Data.USER_STATE_BUTTON][user_language]}: {local.data[user_state][user_language]}\n" \
               f"{local.data[Data.SUBJECT_BUTTON][user_language]}: {local.data[subject_1][user_language]}, " \
               f"{local.data[subject_2][user_language]} "


