from config import Config
from data.models import Quiz, MyEncoder
from ast import literal_eval
import requests
import json
import random
import logging


def json_to_obj(json_obj):
    return Quiz(
        topic=Config.SUBJECT_NAME_DATA[json_obj["topic"]],
        quiz_id=json_obj["quiz_id"],
        question=json_obj["question"],
        options=json_obj["options"].split("$"),
        correct_option_id=json_obj["correct_option_id"],
        owner_id=json_obj["owner"]
    )

# MARK: API interaction


def get_quizzes_from_api():
    logging.info("Start load quizzes from api")
    r = requests.get(Config.API_URL+Config.QUIZ_DB)
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
    return quizzes, quiz_topic


def post_quiz_to_api(quiz):
    r = requests.post(Config.API_URL+Config.QUIZ_DB, json=quiz.to_json())
    logging.info(r)


class QuizService:
    quizzes = {}
    quiz_topic = {}
    quizzes_ids_connection = {}
    correct_option_id = {}

    # MARK: Load quizzes to cash

    def load_quizzes(self):
        self.quizzes, self.quiz_topic = get_quizzes_from_api()

    # MARK: Post quiz to api

    @staticmethod
    def post_quiz(json_obj):
        post_quiz_to_api(json_to_obj(json_obj))

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
