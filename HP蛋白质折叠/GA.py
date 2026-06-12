import random
import numpy as np
from hp_solver import (decode_coords,calc_energy,random_seq,repair_seq,pull_move,apply_pull_moves)

# ─── 算法A：遗传算法 + Pull Move ─────────────────────────────

def ga_pull_move(hp_str, pop_size=60, max_gen=300, pc=0.8, pm=0.3,
                 pm_steps=8, elite_ratio=0.1, seed=None):
    """
    遗传算法 + Pull Move (GA-PM)
    pm: Pull Move变异概率（用Pull Move替代位翻转变异）
    pm_steps: 精英个体每代执行的Pull Move步数
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    n = len(hp_str)
    elite_n = max(1, int(pop_size * elite_ratio))

    # 初始化种群
    pop = []
    while len(pop) < pop_size:
        s = random_seq(n)
        if s:
            pop.append(s)

    def fitness(s):
        return -calc_energy(s, hp_str)

    best_seq = min(pop, key=lambda s: calc_energy(s, hp_str))
    best_e = calc_energy(best_seq, hp_str)
    history = []

    for gen in range(max_gen):
        # 评估
        energies = [calc_energy(s, hp_str) for s in pop]
        fits = [-e + 1 for e in energies]  # 适应度=−E+1（正值）

        # 更新全局最优
        min_e = min(energies)
        if min_e < best_e:
            best_e = min_e
            best_seq = pop[energies.index(min_e)][:]
        history.append(best_e)

        # 精英保留
        sorted_idx = sorted(range(pop_size), key=lambda i: energies[i])
        elites = [pop[i][:] for i in sorted_idx[:elite_n]]

        # 对精英做Pull Move深化
        refined_elites = []
        for e_seq in elites:
            rs, re = apply_pull_moves(e_seq, hp_str, steps=pm_steps)
            refined_elites.append(rs)
            if re < best_e:
                best_e = re
                best_seq = rs[:]

        # 锦标赛选择
        def tournament(k=3):
            candidates = random.sample(range(pop_size), k)
            return pop[min(candidates, key=lambda i: energies[i])][:]

        new_pop = refined_elites[:]
        total_fit = sum(fits)

        while len(new_pop) < pop_size:
            p1 = tournament()
            p2 = tournament()

            # 单点交叉
            if random.random() < pc:
                pt = random.randint(1, n - 2)
                c1 = p1[:pt] + p2[pt:]
                c2 = p2[:pt] + p1[pt:]
            else:
                c1, c2 = p1[:], p2[:]

            # 变异：Pull Move 或 位翻转
            for child in [c1, c2]:
                if random.random() < pm:
                    child_new = pull_move(child, hp_str)
                    if calc_energy(child_new, hp_str) <= calc_energy(child, hp_str):
                        child[:] = child_new
                else:
                    # 普通位翻转变异
                    for i in range(len(child)):
                        if random.random() < 0.05:
                            child[i] = random.randint(0, 3)

                # 修复合法性
                if decode_coords(child) is None:
                    child[:] = repair_seq(child)

            new_pop.extend([c1, c2])

        pop = new_pop[:pop_size]

    return best_seq, best_e, history

