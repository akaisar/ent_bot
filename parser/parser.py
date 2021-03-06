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
    "E": 4,
    "А": 0,
    "С": 2,
    "Е": 4,
    "В": 1,
    "Д": 3,
    "б": 1,
}


def parser(file_name):
    global questions, options, transform_option
    # with codecs.open(file_name, 'rb', 'utf-8') as f:
    #     data = f.read()
    #
    #     questions = re.findall(r"\d+\..+", data)
    with codecs.open(file_name, 'rb', 'utf-8') as f:
        data2 = f.readlines()
        for line in data2:
            if line[0] in transform_option and line[1] == ")":
                options.append(line)
            elif len(line.split()) != 0:
                questions.append(line)
    for i in range(len(options)):
        if i % 5 != transform_option[options[i][0]]:
            print(i/5, options[i])
    with codecs.open("output.txt", "rb", "utf-8") as f:
        data = f.readlines()
        global correct_options
        for i in range(len(data)):
            correct_options[i] = transform_option[data[i][0]]



def get_quizzes(file_name, topic_name):
    # global quizzes
    parser(file_name)
    for i in range(len(questions)):
        quiz = {
            "topic": topic_name,
            "question": questions[i],
            "options": "$".join([option[2:] for option in options[i * 5:(i + 1) * 5]]),
            "correct_option_id": correct_options[i],
            "owner": 0,
            "winners": "1",
            "chat_id": 1,
            "message_id": 1,
        }
        print(quiz)
        r = requests.post(Config.API_URL + 'quizDb', json=json.loads(json.dumps(quiz)))
        print(i, r)


if __name__ == "__main__":
    get_quizzes("input2.txt", "Қазақстан Тарихы")
