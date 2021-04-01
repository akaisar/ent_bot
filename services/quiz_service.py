from config import Config
from data.models import Quiz, MyEncoder, QuizSet
from ast import literal_eval
import requests_async as requests
import json
import random
import logging


def json_to_obj(json_obj):
    return Quiz(
        topic=Config.SUBJECT_NAME_DATA[json_obj["topic"]],
        quiz_id=json_obj["quiz_id"],
        question=json_obj["question"].split("$")[0],
        options=json_obj["options"].split("$"),
        correct_option_id=json_obj["correct_option_id"],
        is_image=json_obj["is_image"]
    )


def json_quiz_set_to_obj(json_obj):
    return QuizSet(
        text=json_obj["text"],
        quizzes=json_obj["questions"]
    )


# MARK: File interaction

def get_image_quizzes_from_file():
    with open("data/quiz_image.txt", "r") as f:
        data = f.read()
    data = json.loads(data)
    quizzes = {}
    quiz_topic = {}
    for json_obj in data:
        topic = Config.SUBJECT_NAME_DATA[json_obj["topic"]]
        quiz_id = json_obj["quiz_id"]
        if topic not in quizzes:
            quizzes[topic] = {}
        quizzes[topic][quiz_id] = json_to_obj(json_obj=json_obj)
        quiz_topic[quiz_id] = topic
        logging.info(quizzes[topic][quiz_id].is_image)
        # print(quizzes[topic][quiz_id].is_image)
    logging.info("Finish load quizzes from api")
    return quizzes, quiz_topic


# MARK: API interaction


async def get_quizzes_from_api():
    logging.info("Start load quizzes from api")
    r = await requests.get(Config.API_URL+Config.QUIZ_DB)
    data = json.loads(r.text)
    quizzes = {}
    quiz_topic = {}
    for json_obj in data:
        topic = Config.SUBJECT_NAME_DATA[json_obj["topic"]]
        quiz_id = json_obj["quiz_id"]
        if topic not in quizzes:
            quizzes[topic] = {}
        quizzes[topic][quiz_id] = json_to_obj(json_obj=json_obj)
        quiz_topic[quiz_id] = topic
    logging.info("Finish load quizzes from api")

    r2 = await requests.get(Config.API_URL+Config.QUIZ_SET_DB)
    data2 = json.loads(r2.text)
    quiz_sets = {}
    quiz_set_topic = {}
    for json_obj in data2:
        quiz_set = json_quiz_set_to_obj(json_obj)
        topic = quiz_topic[quiz_set.quizzes[0]]
        quiz_set_id = json_obj["id"]
        if topic not in quiz_sets:
            quiz_sets[topic] = {}
        quiz_sets[topic][quiz_set_id] = quiz_set
        quiz_set_topic[quiz_set_id] = topic
    return quizzes, quiz_topic, quiz_sets, quiz_set_topic


async def post_quiz_to_api(quiz):
    r = requests.post(Config.API_URL+Config.QUIZ_DB, json=quiz.to_json())
    logging.info(r)


class QuizService:
    quizzes = {}
    quiz_topic = {}
    quizzes_ids_connection = {}
    correct_option_id = {}
    quiz_sets = {}
    quiz_set_topic = {}
    quiz_in_quiz_set = {}

    # MARK: Load quizzes to cash

    async def load_quizzes(self):
        self.quizzes, self.quiz_topic, self.quiz_sets, self.quiz_set_topic = await get_quizzes_from_api()
        for topic, quiz_set_id_quiz_set in self.quiz_sets.items():
            for quiz_set_id, quiz_set in quiz_set_id_quiz_set.items():
                for quiz_id in quiz_set.quizzes:
                    self.quiz_in_quiz_set[quiz_id] = quiz_set_id
    # MARK: Get quiz set

    def get_quiz_sets(self, topic, quiz_number):
        quiz_sets = []
        for quiz_set_id, quiz_set in self.quiz_sets[topic].items():
            quiz_sets.append(quiz_set)
        random.shuffle(quiz_sets)
        cnt = 0
        for index in range(len(quiz_sets)):
            cnt += len(quiz_sets[index].quizzes)
            random.shuffle(quiz_sets[index].quizzes)
            if cnt >= quiz_number:
                return quiz_sets[:index+1]

    def quiz_set_to_quiz_ids(self, quiz_sets, quiz_number):
        quiz_ids = []
        for quiz_set in quiz_sets:
            for quiz in quiz_set.quizzes:
                quiz_ids.append(quiz)
                if len(quiz_ids) == quiz_number:
                    return quiz_ids

    def get_quiz_set_text(self, quiz_id):
        return self.quiz_sets[self.quiz_topic[quiz_id]][self.quiz_in_quiz_set[quiz_id]].text

    # MARK: Post quiz to api

    @staticmethod
    def post_quiz(json_obj):
        post_quiz_to_api(json_to_obj(json_obj))

    def is_in_quiz_set(self, quiz_id):
        return quiz_id in self.quiz_in_quiz_set

    # MARK: Return quiz by quiz_id

    def get_quiz_from_id(self, quiz_id):
        return self.quizzes[self.quiz_topic[quiz_id]][quiz_id]

    # MARK: Return specified number of quizzes by topic

    def get_specified_number_of_quizzes_by_topic(self, topic_name, number):
        quiz_ids = []
        for quiz_id, quiz in self.quizzes[topic_name].items():
            quiz_ids.append(quiz_id)
        random.shuffle(quiz_ids)
        return quiz_ids[:min(number, len(quiz_ids))]

    # MARK: Quiz ids connection

    def connect_ids(self, new_id, old_id):
        self.quizzes_ids_connection[new_id] = old_id

    # MARK: Get quiz id in DB

    def get_old_id(self, new_id):
        return self.quizzes_ids_connection[new_id]

    # MARK: Check option

    def is_option_correct(self, option, quiz_id):
        return self.correct_option_id[quiz_id] == option

    # MARK: Set correct option

    def set_correct_option_id(self, quiz_id, option_id):
        self.correct_option_id[quiz_id] = option_id

    # MARK: Shuffle options

    @staticmethod
    def shuffle_options(options, correct_option_id):
        correct_option = options[correct_option_id]
        random.shuffle(options)
        for i in range(len(options)):
            if options[i] == correct_option:
                return options, i
