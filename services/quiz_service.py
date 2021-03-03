from config import Config
from data.models import Quiz, MyEncoder
from ast import literal_eval
import requests
import json
import random


def get_request_from_api(suffix):
    return requests.get(Config.API_URL + suffix)


class QuizService:
    quizzes_from_topic = {}
    quizzes_ids_connection = {}

    def load_quizzes_from_topic(self, topic_name):
        if topic_name in self.quizzes_from_topic:
            return self.quizzes_from_topic[topic_name]
        quizzes = []
        data = get_request_from_api(f'quizDb/{topic_name}/')
        print(data.text)
        for detail in json.loads(data.text):
            print(detail)
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
        self.quizzes_from_topic[topic_name] = quizzes
        return quizzes

    def load_few_quizzes_from_topic(self, topic_name, number):
        quizzes = self.load_quizzes_from_topic(topic_name=topic_name)
        random.shuffle(quizzes)
        if len(quizzes) == 0:
            return []
        return quizzes[:min(number+1, len(quizzes))]

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
        print(r)

    def connect_ids(self, new_id, old_id):
        self.quizzes_ids_connection[new_id] = old_id

    def get_old_id(self, new_id):
        return self.quizzes_ids_connection[new_id]

    def is_option_correct(self, option, quiz_id):
        for topic, quizzes in self.quizzes_from_topic.items():
            for quiz in quizzes:
                if quiz.quiz_id == quiz_id:
                    return quiz.correct_option_id == option
