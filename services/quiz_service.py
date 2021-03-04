from config import Config
from data.models import Quiz, MyEncoder
from ast import literal_eval
import requests
import json
import random
import logging


def get_request_from_api(suffix):
    return requests.get(Config.API_URL + suffix)


class QuizService:
    quizzes_from_topic = {}
    quizzes_ids_connection = {}
    correct_option_id = {}

    def load_quizzes_from_topic(self, topic_name):
        if topic_name in self.quizzes_from_topic:
            return self.quizzes_from_topic[topic_name]
        quizzes = []
        data = get_request_from_api(f'quizDb/{topic_name}/')
        cnt_quizzes = 0
        for detail in json.loads(data.text):
            if len(detail["options"].split("$")) < 2:
                continue
            cnt_quizzes += 1
            try:
                quiz = Quiz(
                    topic=detail["topic"],
                    quiz_id=detail["quiz_id"],
                    question=detail["question"],
                    options=detail["options"].split("$"),
                    correct_option_id=detail["correct_option_id"],
                    owner_id=detail["owner"]
                )
                quizzes.append(quiz)
            except Exception as e:
                print(e)
        logging.info(cnt_quizzes)
        logging.info(len(quizzes))
        self.quizzes_from_topic[topic_name] = quizzes
        return quizzes

    def load_few_quizzes_from_topic(self, topic_name, number):
        quizzes = self.load_quizzes_from_topic(topic_name=topic_name)
        random.shuffle(quizzes)
        if len(quizzes) == 0:
            return []
        return quizzes[:min(number, len(quizzes))]

    def push_quiz_to_api(self, topic, quiz_id, question, options, correct_option_id, owner_id):
        quiz = Quiz(
            topic=topic,
            quiz_id=quiz_id,
            question=question,
            options=options,
            correct_option_id=correct_option_id,
            owner_id=owner_id
        )
        if quiz.topic in self.quizzes_from_topic:
            self.quizzes_from_topic[quiz.topic].append(quiz)
        else:
            self.quizzes_from_topic[quiz.topic] = []
            self.quizzes_from_topic[quiz.topic].append(quiz)
        quiz_json = {
            "topic": topic,
            "quiz_id": quiz_id,
            "question": question,
            "options": "$".join(options),
            "correct_option_id": correct_option_id,
            "owner": owner_id,
            "winners": "1",
            "chat_id": 1,
            "message_id": 1,
        }
        print(json.dumps(quiz_json))
        print("post quiz to api")
        r = requests.post(Config.API_URL+'quizDb', json=json.loads(json.dumps(quiz_json)))
        logging.info(r)
        return r

    def connect_ids(self, new_id, old_id):
        self.quizzes_ids_connection[new_id] = old_id

    def get_old_id(self, new_id):
        return self.quizzes_ids_connection[new_id]

    def is_option_correct(self, option, quiz_id):
        return self.correct_option_id[quiz_id] == option

    def post_correct_option_id(self, quiz_id, option_id):
        self.correct_option_id[quiz_id] = option_id

    @staticmethod
    def shuffle_options(options, correct_option_id):
        correct_option = options[correct_option_id]
        random.shuffle(options)
        for i in range(len(options)):
            if options[i] == correct_option:
                return options, i
