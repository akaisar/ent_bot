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


def get_request_from_api(suffix):
    return requests.get(Config.API_URL + suffix)

topics = ["Қазақ тілі", "Қазақстан Тарихы", "История Казахстана", "География рус"]
for topic in topics:
    data = get_request_from_api(f"quizDb/{topic}/")
    data = json.loads(data.text)
    for line in data:
        output.append(str(line))
with open('local_db.txt', "w") as f:
    f.writelines(output)