import random
import numpy as np
from hp_solver import (calc_energy,random_seq,apply_pull_moves,DIRS)

# ─── 算法B：蚁群算法 + Pull Move ─────────────────────────────

def aco_pull_move(hp_str, n_ants=30, max_iter=200, alpha=1.0, beta=2.0,
                  rho=0.1, Q=1.0, pm_steps=8, seed=None):
    """
    蚁群算法 + Pull Move (ACO-PM)
    每只蚂蚁构造完整路径后，执行Pull Move局部优化
    信息素更新：蒸发+最优蚂蚁加强
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    n = len(hp_str)
    # 信息素：每步(step) × 每方向(4) 的矩阵
    tau = np.ones((n - 1, 4)) * 0.5

    best_seq = random_seq(n)
    best_e = calc_energy(best_seq, hp_str)
    history = []

    def heuristic(step, direction, coords, hp_str):
        """启发式：下一步如果是H，检查H邻居数"""
        if step + 1 >= n:
            return 1.0
        x, y = coords[-1][0] + DIRS[direction][0], coords[-1][1] + DIRS[direction][1]
        if hp_str[step + 1] != 'H':
            return 1.0
        h_nb = 0
        coord_set = set(coords)
        for dx, dy in DIRS:
            nb = (x + dx, y + dy)
            if nb in coord_set:
                idx = list(coords).index(nb)  # 近似，避免歧义
                if idx < len(hp_str) and hp_str[idx] == 'H':
                    h_nb += 1
        return max(1.0, h_nb + 1)

    for it in range(max_iter):
        ant_seqs = []
        ant_energies = []

        for _ in range(n_ants):
            # 构造路径
            seq = []
            coords = [(0, 0)]
            coord_set = {(0, 0)}
            ok = True
            for step in range(n - 1):
                cx, cy = coords[-1]
                # 可行方向
                feasible = []
                for d in range(4):
                    nx, ny = cx + DIRS[d][0], cy + DIRS[d][1]
                    if (nx, ny) not in coord_set:
                        feasible.append(d)
                if not feasible:
                    ok = False
                    break
                # 计算选择概率
                probs = []
                for d in feasible:
                    eta = heuristic(step, d, coords, hp_str)
                    probs.append((tau[step][d] ** alpha) * (eta ** beta))
                total = sum(probs)
                probs = [p / total for p in probs]
                # 轮盘赌选择
                r = random.random()
                cumsum = 0.0
                chosen = feasible[-1]
                for d, p in zip(feasible, probs):
                    cumsum += p
                    if r <= cumsum:
                        chosen = d
                        break
                seq.append(chosen)
                nx, ny = cx + DIRS[chosen][0], cy + DIRS[chosen][1]
                coords.append((nx, ny))
                coord_set.add((nx, ny))

            if not ok:
                s = random_seq(n)
                if s is None:
                    continue
                seq = s

            # Pull Move 后优化
            opt_seq, opt_e = apply_pull_moves(seq, hp_str, steps=pm_steps)
            ant_seqs.append(opt_seq)
            ant_energies.append(opt_e)

            if opt_e < best_e:
                best_e = opt_e
                best_seq = opt_seq[:]

        history.append(best_e)

        if not ant_seqs:
            continue

        # 信息素更新
        tau *= (1 - rho)
        # 找本轮最优蚂蚁
        best_ant_idx = ant_energies.index(min(ant_energies))
        best_ant_seq = ant_seqs[best_ant_idx]
        best_ant_e = ant_energies[best_ant_idx]
        delta = Q / (-best_ant_e + 1e-6) if best_ant_e < 0 else Q * 0.1
        for step, d in enumerate(best_ant_seq):
            if step < n - 1:
                tau[step][d] += delta

        # 信息素下界
        tau = np.clip(tau, 0.01, 10.0)

    return best_seq, best_e, history


