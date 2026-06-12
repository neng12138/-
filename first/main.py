import random
import math

# 问题数据
weights = [2, 3, 5, 1, 4]  # 物品的重量
values = [2, 5, 8, 3, 6]  # 物品的价值
capacity = 10  # 背包容量 （0-1背包）
n = len(weights)  # 物品数量

# 此函数用于计算当前solution的装配方式得到的价值，若超重则返回价值为0
def fitness(solution):
    """
    solution - 表示物品的选择状态（ 1表示选择 ， 0表示不选 ）
    """
    total_weight = sum(weights[i] * solution[i] for i in range(n))  # 计算此时的总重量
    total_value = sum(values[i] * solution[i] for i in range(n))  # 计算此时的总价值
    if total_weight > capacity:     # 超重 （给予惩罚）
        return 0
    return total_value

# 此函数用于产生一个新的邻域解
def generate_neighbor(current_solution):
    """
    current_solution - 当前解
    """
    solution = current_solution.copy()
    i = random.randint(0, n - 1)  # 随机选择一个物品
    solution[i] = 1 - solution[i]   # 若已装配则取出，若未装配则放入背包
    return solution

# 此函数用于执行模拟退火，返回最优解和此时的最优价值
def simulated_annealing(initial_temp, final_temp, cooling_rate, max_iter):
    """
        initial_temp - 初始温度
        final_temp - 最终温度
        cooling_rate - 冷却速率（温度衰减系数）
        max_iter - 每个温度下的迭代次数
    """
    # 初始化生成一个初始解 （ 随机即可 ）
    current_solution = [random.randint(0, 1) for _ in range(n)]
    current_value = fitness(current_solution)  # 计算当前价值，超重则为0

    best_solution = current_solution.copy()  # 记录此时最优的装配情况 （后续更新）
    best_value = current_value  # 记录此时最优的价值 （后续更新）

    temperature = initial_temp # 记录当前温度（后续更新）
    history = []  # 记录搜索历史 （方便后续控制台输出，若不要输出，可以修改函数移除history）

    print("开始模拟退火算法...")
    print(f"初始解: {current_solution}, 价值: {current_value}")
    print("-" * 50)
    # 温度下降过程 （ 外循环 ）
    while temperature > final_temp:  # （不断退火）

        for _ in range(max_iter):  # 在当前温度下进行多次搜索 （内循环）
            # 生成邻域解 （ 随机更换一个物品的状态 ）
            neighbor = generate_neighbor(current_solution)
            neighbor_value = fitness(neighbor)

            # 计算价值差 （ 判断此解会不会更优 ）
            delta = neighbor_value - current_value   # 直接比也行
            if delta > 0:      # 此解更优，更新当前的 装配状态 和 背包的价值 （直接接受）
                current_solution = neighbor
                current_value = neighbor_value
                if current_value > best_value:  # 判断是不是最好的
                    best_solution = current_solution.copy()
                    best_value = current_value
            else:   # 如果邻居解更差，以一定概率接受
                probability = math.exp(delta / temperature) # 概率计算公式：P = exp(delta / temperature)
                if random.random() < probability:
                    current_solution = neighbor
                    current_value = neighbor_value

        history.append((temperature, best_value))  # 记录当前温度下的最优值，后续控制台输出
        # 温度更新：线性冷却或指数冷却
        temperature *= cooling_rate  # 使用指数冷却：T = T * cooling_rate
        
        if len(history) % 10 == 0:  # 每10次迭代打印查看当前的最优情况 （方便控制台输出） 
            print(f"温度: {temperature:.4f}, 当前最优价值: {best_value}")   # 打印进度

    # 打印最终搜索到的最优情况
    print("-" * 50)
    print(f"算法结束，最优解: {best_solution}")
    print(f"总重量: {sum(weights[i] * best_solution[i] for i in range(n))}")
    print(f"总价值: {best_value}")


# 运行函数
def main():
    # 设置模拟退火参数
    initial_temp = 100  # 初始温度
    final_temp = 0.01  # 最终温度
    cooling_rate = 0.9  # 冷却速率（每次乘以0.9）
    max_iter = 100  # 每个温度下的迭代次数

    simulated_annealing(   # 运行算法
        initial_temp, final_temp, cooling_rate, max_iter
    )

if __name__ == "__main__":
    random.seed(42)  # 设置随机种子，便于结果复现
    main()