import re
import json
import requests
from config import Config
# with open("3683_testent_history.rtf") as f:
#     data = f.read()
#     options = re.findall(r'\\b .+', data)
#     # print(len(options))
#     # for option in options:
#     #     print(option)
#
# with open("history_rus_correct_ans.txt", "w") as f:
#     for option in options:
#         f.write(option+"\n")
ans = {}
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
}
output = []
options = [1, 3, 3, 4, 0, 1, 4, 4, 3, 0, 1, 2, 3, 1, 2, 1, 1, 1, 3, 3]
options2 = [2, 2, 4, 1, 0, 1, 4, 3, 0, 0, 0, 1, 0, 4, 2, 1, 4, 1, 3, 1]

for index in range(len(options)):
    op = options[index]
    question = {
        "topic": "Математика rus",
        "question": f"8104_Математика rus_{index+1}",
        "options": "5",
        "correct_option_id": op,
        "owner": 0,
        "winners": "1",
        "message_id": 1,
    }
    r = requests.post(Config.API_URL + Config.QUIZ_DB, json=question)
    print(r.text)
# with open("local_db_3.txt", "r") as f:
#     data = f.read()
#     data = json.loads(data)
#     cnt = 0
#     sz = len(data)
#     for json_quiz in data:
#         json_quiz2 = {
#             "topic": json_quiz["topic"],
#             "question": json_quiz["question"],
#             "options": json_quiz["options"],
#             "correct_option_id": json_quiz["correct_option_id"],
#             "owner": 0,
#             "winners": "1",
#             "message_id": 1,
#         }
#         print(json_quiz2)
#         cnt += 1
#         print(cnt*100/sz, "%")
#         r = requests.post(Config.API_URL + Config.QUIZ_DB, json=json_quiz2)
#         print(r.text)