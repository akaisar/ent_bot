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
output = []


with open("input.txt") as f, open("output.txt", "w") as f2:
    data = f.readlines()
    for line in data:
        output.append(str(transform_option[line[0]]) + "\n")
    f2.writelines(output)
