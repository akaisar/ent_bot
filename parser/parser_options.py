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

# with open("local_db_2.txt", "r") as f:
#     data = f.read()
#     data = json.loads(data)
#     for json_quiz in data:
#         json_quiz2 = {
#             "topic": json_quiz["topic"],
#             "question": json_quiz["question"],
#             "options": json_quiz["options"],
#             "correct_option_id": json_quiz["correct_option_id"],
#             "owner": 0,
#             "winners": "1",
#             "chat_id": 1,
#             "message_id": 1,
#         }
#         print(json_quiz2)
#         r = requests.post(Config.API_URL + 'quizDb', json=json_quiz2)
#         print(r)