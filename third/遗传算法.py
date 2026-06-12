import numpy as np


# 定义目标函数
def fitness(x1, x2, x3, x4):
    return 1 / (x1 ** 2 + x2 ** 2 + x3 ** 2 + x4 ** 2 + 1)


# 参数设置
pop_size = 50  # 种群大小
n_generations = 50  # 迭代代数
n_vars = 4  # 变量个数
bounds = [-5, 5]  # 变量范围
pc = 0.8  # 交叉概率
pm = 0.1  # 变异概率
elite_size = 2  # 精英保留数量


# 初始化种群
def init_population():
    return np.random.uniform(bounds[0], bounds[1], (pop_size, n_vars))

# 计算适应度
def evaluate(population):
    fitness_values = []
    for ind in population:
        y = fitness(ind[0], ind[1], ind[2], ind[3])
        fitness_values.append(y)
    return np.array(fitness_values)


# 轮盘赌选择
def roulette_select(population, fitness_values):
    probs = fitness_values / np.sum(fitness_values)
    idx = np.random.choice(pop_size, p=probs)
    return population[idx].copy()


# 算术交叉
def crossover(parent1, parent2):
    if np.random.rand() < pc:
        alpha = np.random.rand()
        child1 = alpha * parent1 + (1 - alpha) * parent2
        child2 = alpha * parent2 + (1 - alpha) * parent1
        return child1, child2
    return parent1.copy(), parent2.copy()


# 均匀变异
def mutate(individual):
    for i in range(n_vars):
        if np.random.rand() < pm:
            individual[i] += np.random.uniform(-0.5, 0.5)
            individual[i] = np.clip(individual[i], bounds[0], bounds[1])
    return individual

# 主循环
population = init_population()
best_solution = None
best_fitness = -np.inf


for generation in range(n_generations):
    # 评估
    fitness_values = evaluate(population)

    # 记录最优解
    current_best_idx = np.argmax(fitness_values)
    current_best_fitness = fitness_values[current_best_idx]
    current_best_solution = population[current_best_idx]

    if current_best_fitness > best_fitness:
        best_fitness = current_best_fitness
        best_solution = current_best_solution.copy()

    # 打印每代信息
    avg_fitness = np.mean(fitness_values)
    print(f"第{generation + 1:2d}代 -- 最优适应度: {current_best_fitness:.6f}  "
          f"最优解: {current_best_solution.round(4)}")

    # 生成下一代
    new_population = []
    # 精英保留
    elite_indices = np.argsort(fitness_values)[-elite_size:]
    for idx in elite_indices:
        new_population.append(population[idx].copy())

    # 生成其余个体
    while len(new_population) < pop_size:
        # 选择父代
        parent1 = roulette_select(population, fitness_values)
        parent2 = roulette_select(population, fitness_values)

        # 交叉
        child1, child2 = crossover(parent1, parent2)

        # 变异
        child1 = mutate(child1)
        child2 = mutate(child2)

        new_population.extend([child1, child2])
    population = np.array(new_population[:pop_size])

print("-" * 60)
print("最优解:")
print(f"  x1 = {best_solution[0]:.6f}")
print(f"  x2 = {best_solution[1]:.6f}")
print(f"  x3 = {best_solution[2]:.6f}")
print(f"  x4 = {best_solution[3]:.6f}")
print(f"最大值 y = {best_fitness:.6f}")
