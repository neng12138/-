import random
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
# 遗传算法
from GA import ga_pull_move
# 蚁群算法
from ACO import aco_pull_move
# 可视化工具
from Vision import plot_conformation, plot_convergence

rcParams['font.family'] = 'SimHei'
rcParams['axes.unicode_minus'] = False


# ─── 主程序 ───────────────────────────────────────────────────

# 测试序列
SEQUENCES = {
    "20mer": "HPHPPHHPHPPHPHHPPHPH",
    "24mer": "HHPPHPPHPPHPPHPPHPPHPPHH"
}

def run_all():
    results = {}
    random.seed(42)
    np.random.seed(42)

    print("=" * 55)
    print("HP格点模型蛋白质折叠求解")
    print("算法A：遗传算法 + Pull Move（GA-PM）")
    print("算法B：蚁群算法 + Pull Move（ACO-PM）")
    print("=" * 55)

    for name, seq_str in SEQUENCES.items():
        print(f"\n--- 序列 {name}: {seq_str} ---")
        results[name] = {}

        # 算法A: GA-PM（多次运行取最优）
        t0 = time.time()
        ga_best_e = 0
        ga_best_seq = None
        ga_best_hist = None
        for run in range(3):
            ga_seq, ga_e, ga_hist = ga_pull_move(
                seq_str, pop_size=120, max_gen=2000,
                pc=0.8, pm=0.15, pm_steps=24, elite_ratio=0.2, seed=42 + run)
            if ga_e < ga_best_e:
                ga_best_e = ga_e
                ga_best_seq = ga_seq
                ga_best_hist = ga_hist
        ga_time = time.time() - t0
        print(f"  GA-PM  最优能量: {ga_best_e}  用时: {ga_time:.1f}s")

        # 算法B: ACO-PM（多次运行取最优）
        t0 = time.time()
        aco_best_e = 0
        aco_best_seq = None
        aco_best_hist = None
        for run in range(3):
            aco_seq, aco_e, aco_hist = aco_pull_move(
                seq_str, n_ants=80, max_iter=2000, alpha=0.9, beta=1.9,
                rho=0.1, Q=1.0, pm_steps=18, seed=42 + run)
            if aco_e < aco_best_e:
                aco_best_e = aco_e
                aco_best_seq = aco_seq
                aco_best_hist = aco_hist
        aco_time = time.time() - t0
        print(f"  ACO-PM 最优能量: {aco_best_e}  用时: {aco_time:.1f}s")

        results[name] = {
            "ga_seq": ga_best_seq, "ga_e": ga_best_e,
            "ga_hist": ga_best_hist, "ga_time": ga_time,
            "aco_seq": aco_best_seq, "aco_e": aco_best_e,
            "aco_hist": aco_best_hist, "aco_time": aco_time,
            "hp": seq_str
        }

    return results

def generate_figures(results):
    """生成所有图表并保存"""
    fig_paths = {}
    seq_names = list(results.keys())

    # ── 图1：两序列收敛曲线（2×2子图）
    fig1, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    fig1.suptitle("两种算法收敛曲线对比", fontsize=13, fontweight='bold')
    for ax, name in zip(axes, seq_names):
        r = results[name]
        plot_convergence(
            [r["ga_hist"], r["aco_hist"]],
            ["GA-PM（遗传算法）", "ACO-PM（蚁群算法）"],
            ["#534AB7", "#0F6E56"],
            title=f"序列 {name}",
            ax=ax
        )
    plt.tight_layout()
    path1 = "./picture/fig_convergence.png"
    fig1.savefig(path1, dpi=150, bbox_inches='tight')
    plt.close(fig1)
    fig_paths["convergence"] = path1
    print(f"  已保存: {path1}")

    # ── 图2：最优构型（2行×2列）
    fig2, axes2 = plt.subplots(2, 2, figsize=(10, 10))
    fig2.suptitle("最优折叠构型", fontsize=13, fontweight='bold')
    for col, name in enumerate(seq_names):
        r = results[name]
        plot_conformation(r["ga_seq"], r["hp"],
                          title=f"GA-PM  {name}", ax=axes2[0][col])
        plot_conformation(r["aco_seq"], r["hp"],
                          title=f"ACO-PM  {name}", ax=axes2[1][col])
    plt.tight_layout()
    path2 = "./picture/fig_conformation.png"
    fig2.savefig(path2, dpi=150, bbox_inches='tight')
    plt.close(fig2)
    fig_paths["conformation"] = path2
    print(f"  已保存: {path2}")

    # ── 图3：能量对比柱状图
    fig3, ax3 = plt.subplots(figsize=(7, 4.5))
    x = np.arange(len(seq_names))
    width = 0.3
    ga_energies = [results[n]["ga_e"] for n in seq_names]
    aco_energies = [results[n]["aco_e"] for n in seq_names]
    b1 = ax3.bar(x - width / 2, ga_energies, width, label="GA-PM",
                 color="#534AB7", alpha=0.85)
    b2 = ax3.bar(x + width / 2, aco_energies, width, label="ACO-PM",
                 color="#0F6E56", alpha=0.85)
    ax3.bar_label(b1, padding=3, fontsize=10)
    ax3.bar_label(b2, padding=3, fontsize=10)
    ax3.set_xticks(x)
    ax3.set_xticklabels(seq_names, fontsize=12)
    ax3.set_ylabel("最优能量", fontsize=11)
    ax3.set_title("两序列最优能量对比", fontsize=12)
    ax3.legend(fontsize=10)
    ax3.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    path3 = "./picture/fig_energy_compare.png"
    fig3.savefig(path3, dpi=150, bbox_inches='tight')
    plt.close(fig3)
    fig_paths["energy_compare"] = path3
    print(f"  已保存: {path3}")

    # ── 图4：运行时间对比柱状图
    fig4, ax4 = plt.subplots(figsize=(7, 4))
    ga_times = [results[n]["ga_time"] for n in seq_names]
    aco_times = [results[n]["aco_time"] for n in seq_names]
    b3 = ax4.bar(x - width / 2, ga_times, width, label="GA-PM", color="#534AB7", alpha=0.85)
    b4 = ax4.bar(x + width / 2, aco_times, width, label="ACO-PM", color="#0F6E56", alpha=0.85)
    ax4.bar_label(b3, fmt="%.1f s", padding=3, fontsize=9)
    ax4.bar_label(b4, fmt="%.1f s", padding=3, fontsize=9)
    ax4.set_xticks(x)
    ax4.set_xticklabels(seq_names, fontsize=12)
    ax4.set_ylabel("运行时间（秒）", fontsize=11)
    ax4.set_title("两序列运行时间对比", fontsize=12)
    ax4.legend(fontsize=10)
    ax4.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    path4 = "./picture/fig_time_compare.png"
    fig4.savefig(path4, dpi=150, bbox_inches='tight')
    plt.close(fig4)
    fig_paths["time_compare"] = path4
    print(f"  已保存: {path4}")

    return fig_paths

# ─── 运行 ───────────────────────────────────────────────────

if __name__ == "__main__":
    print("正在运行实验，请稍候...\n")
    results = run_all()

    print("\n正在生成图表...")
    fig_paths = generate_figures(results)



