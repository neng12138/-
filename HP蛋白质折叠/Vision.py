import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rcParams
from hp_solver import (decode_coords,calc_energy,DIRS)

rcParams['font.family'] = 'SimHei'
rcParams['axes.unicode_minus'] = False

# ─── 可视化工具 ───────────────────────────────────────────────

def plot_conformation(seq, hp_str, title="", ax=None):
    """绘制蛋白质构型"""
    coords = decode_coords(seq)
    if coords is None:
        return
    xs = [c[0] for c in coords]
    ys = [c[1] for c in coords]
    if ax is None:
        fig, ax = plt.subplots(figsize=(4, 4))

    # 绘制骨架
    ax.plot(xs, ys, 'k-', linewidth=1.2, zorder=1)

    # 绘制节点
    for i, (x, y) in enumerate(coords):
        color = '#E24B4A' if hp_str[i] == 'H' else '#378ADD'
        ax.scatter(x, y, c=color, s=180, zorder=2, edgecolors='white', linewidths=0.8)

    # 绘制H-H接触
    coord_idx = {c: i for i, c in enumerate(coords)}
    for i, (x, y) in enumerate(coords):
        if hp_str[i] != 'H':
            continue
        for dx, dy in DIRS:
            nb = (x + dx, y + dy)
            if nb in coord_idx:
                j = coord_idx[nb]
                if j > i + 1 and hp_str[j] == 'H':
                    ax.plot([x, nb[0]], [y, nb[1]], '--',
                            color='#BA7517', linewidth=1.2, alpha=0.7, zorder=0)

    energy = calc_energy(seq, hp_str)
    ax.set_title(f"{title}\nE={energy}", fontsize=11)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.2)
    ax.axis('off')

    h_patch = mpatches.Patch(color='#E24B4A', label='H（疏水）')
    p_patch = mpatches.Patch(color='#378ADD', label='P（亲水）')
    ax.legend(handles=[h_patch, p_patch], fontsize=7, loc='best')

def plot_convergence(histories, labels, colors, title="收敛曲线", ax=None):
    """绘制收敛曲线"""
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 4))
    for hist, label, color in zip(histories, labels, colors):
        ax.plot(hist, label=label, color=color, linewidth=1.5)
    ax.set_xlabel("迭代次数", fontsize=11)
    ax.set_ylabel("最优能量", fontsize=11)
    ax.set_title(title, fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)


