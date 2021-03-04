import codecs
import re
import requests
import json
from config import Config
questions = []
options = []
correct_options = {}
transform_option = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4
}


def parser(file_name):
    with codecs.open(file_name, 'rb', 'utf-8') as f:
        data = f.read()
        global questions, options, correct_options, transform_option
        questions = re.findall(r"\d+\..+", data)
        options = re.findall(r"[A-E]\).+", data)
        correct_options_value = re.findall(r"\d+ [A-E]\)", data)
        for c_option in correct_options_value:
            id = re.findall(r"\d*", c_option)[0]
            value = re.findall("[A-E]", c_option)[0]
            correct_options[int(id) - 1] = transform_option[value]


def get_quizzes(file_name, topic_name):
    global quizzes
    parser(file_name)
    for i in range(len(questions)):
        quiz = {
            "topic": topic_name,
            "question": "".join(re.split(r"\d+\.", questions[i])),
            "options": "$".join(["".join(re.split(r"[A-E]\) ", option)) for option in options[i * 5:(i + 1) * 5]]),
            "correct_option_id": correct_options[i],
            "owner": 0,
            "winners": "1",
            "chat_id": 1,
            "message_id": 1,
        }
        print(quiz)
        r = requests.post(Config.API_URL + 'quizDb', json=json.loads(json.dumps(quiz)))
        print(r)


if __name__ == "__main__":
    get_quizzes("kazakh_language.txt", "Қазақ тілі")