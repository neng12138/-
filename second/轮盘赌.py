# import random

# # 轮盘赌的结果 (颜色, 概率)
# text = {
#     "red" : 0.2,
#     "green" : 0.3,
#     "blue" : 0.1,
#     "yellow" : 0.4,
# }

# random_possible = random.random()   # 生成一个0到1之间的随机数
# sum_possible = 0
# for i in text:
#     sum_possible += text[i]
#     if random_possible <= sum_possible:
#         print(i)
#         break

import random

def roulette(list_possible:list) -> int:
    random_possible = random.random()
    sum_possible = 0
    for i in range(len(list_possible)):
        sum_possible += list_possible[i]
        if random_possible <= sum_possible:
            return i   # 返回对应的索引值

print(roulette([0.2, 0.3, 0.1, 0.4]))
