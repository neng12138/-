import numpy as np

# 距离矩阵
dist = np.array([
    [np.inf, 3, 1, 2],
    [3, np.inf, 5, 4],
    [1, 5, np.inf, 2],
    [2, 4, 2, np.inf]
])

# 城市名称
cities = ['A', 'B', 'C', 'D']

# 参数设置
m = 3  # 蚂蚁数量
alpha = 1  # 信息素重要性因子
beta = 2  # 启发因子重要性因子
rho = 0.5  # 信息素挥发率
Q = 1  # 信息素常数
iterations = 10  # 迭代次数

# 初始化信息素矩阵（对称矩阵）
pheromone = np.ones((4, 4)) * 0.1
np.fill_diagonal(pheromone, 0)  # 对角线设为0


def calculate_distance(path):
    """计算路径总距离"""
    total_dist = 0
    for i in range(len(path) - 1):
        total_dist += dist[path[i], path[i + 1]]
    total_dist += dist[path[-1], path[0]]  # 返回起点
    return total_dist


def select_next_city(current, visited, pheromone, dist):
    """根据概率选择下一个城市"""
    unvisited = [c for c in range(4) if c not in visited]
    probabilities = []

    for next_city in unvisited:
        tau = pheromone[current, next_city] ** alpha
        eta = (1.0 / dist[current, next_city]) ** beta
        probabilities.append(tau * eta)

    # 归一化
    probabilities = np.array(probabilities)
    probs = probabilities / probabilities.sum()

    # 轮盘赌选择
    return np.random.choice(unvisited, p=probs)


def ant_cycle():
    """一只蚂蚁完成一次完整路径"""
    # 随机选择起点
    start = np.random.randint(0, 4)
    path = [start]
    visited = {start}

    # 逐步选择下一个城市
    current = start
    for _ in range(3):
        next_city = select_next_city(current, visited, pheromone, dist)
        path.append(next_city)
        visited.add(next_city)
        current = next_city

    # 计算路径长度
    length = calculate_distance(path)
    return path, length


# 主循环
best_path = None
best_length = np.inf

for iteration in range(iterations):
    # 存储所有蚂蚁的路径和长度
    paths = []
    lengths = []

    # 每只蚂蚁构建路径
    for ant in range(m):
        path, length = ant_cycle()
        paths.append(path)
        lengths.append(length)

        # 更新全局最优解
        if length < best_length:
            best_length = length
            best_path = path.copy()

    # 更新信息素
    pheromone = pheromone * (1 - rho)  # 挥发

    # 添加蚂蚁释放的信息素
    for path, length in zip(paths, lengths):
        delta = Q / length
        for i in range(len(path) - 1):
            pheromone[path[i], path[i + 1]] += delta
            pheromone[path[i + 1], path[i]] += delta
        # 返回起点的边
        pheromone[path[-1], path[0]] += delta
        pheromone[path[0], path[-1]] += delta

    # 输出迭代信息
    avg_length = np.mean(lengths)
    min_length = min(lengths)
    print(f"迭代 {iteration + 1:2d} | 最佳路径长度: {min_length:.2f}")

print("-" * 50)
print("最优路径:", ' -> '.join([cities[i] for i in best_path]) + f" -> {cities[best_path[0]]}")
print(f"最优路径长度: {best_length:.2f}")
