import re
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

with open("history_rus_correct_ans.txt") as f, open("history_rus_correct_options.txt", "w") as f2:
    data = f.readlines()
    for i in range(len(data)):
        f2.write(str(transform_option[data[i][0]])+'\n')