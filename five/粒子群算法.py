import numpy as np


# 设置目标函数
def fitness(x):
    """适应度函数（目标函数）"""
    return x[0]**2 + x[1]**2


# 参数设置
N_PARTICLES = 30      # 粒子数量
N_DIM = 2             # 维度
MAX_ITER = 100        # 最大迭代次数
BOUNDS = [-10.0, 10.0]  # 变量范围

# 超参数
w = 0.5      # 惯性权重
c1 = 1.5     # 个体学习因子
c2 = 1.5     # 社会学习因子

# 初始化
positions = np.random.uniform(BOUNDS[0], BOUNDS[1], (N_PARTICLES, N_DIM))
velocities = np.random.uniform(-1, 1, (N_PARTICLES, N_DIM))
personal_best_positions = positions.copy()
personal_best_scores = np.array([fitness(p) for p in positions])
global_best_position = personal_best_positions[np.argmin(personal_best_scores)]
global_best_score = np.min(personal_best_scores)

# 初始化的粒子信息
print(f"初始全局最优值 = {global_best_score:.4f}  初始参数值 = {global_best_position}")


# 迭代寻优
for t in range(1, MAX_ITER + 1):
    # 更新粒子速度和位置
    r1 = np.random.random((N_PARTICLES, N_DIM))
    r2 = np.random.random((N_PARTICLES, N_DIM))
    velocities = (w * velocities +
                  c1 * r1 * (personal_best_positions - positions) +
                  c2 * r2 * (global_best_position - positions))
    positions = positions + velocities

    # 边界处理（将超出边界的粒子拉回边界）
    positions = np.clip(positions, BOUNDS[0], BOUNDS[1])

    # 评估适应度函数值
    scores = np.array([fitness(p) for p in positions])

    # 更新个体最优
    improved = scores < personal_best_scores
    personal_best_positions[improved] = positions[improved]
    personal_best_scores[improved] = scores[improved]

    # 更新全局最优
    current_best_idx = np.argmin(personal_best_scores)
    if personal_best_scores[current_best_idx] < global_best_score:
        global_best_score = personal_best_scores[current_best_idx]
        global_best_position = personal_best_positions[current_best_idx]

    # 输出迭代信息
    if t % 5 == 0 or t == MAX_ITER:
        print(f"迭代 {t:3d} : 全局最优值 = {global_best_score:.4f}  参数值 = {global_best_position}")

    # 适应度值足够小时提前终止
    if global_best_score < 1e-9:
        break


print("\n最终结果：")
print(f"最优参数值：({global_best_position[0]:.4f}, {global_best_position[1]:.4f})")
print(f"最小值：{global_best_score:.4f}")


