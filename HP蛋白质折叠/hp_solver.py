import random

# ─── HP模型基础 ───────────────────────────────────────────────

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 上右下左

def decode_coords(seq):
    """方向序列 -> 格点坐标列表，返回None表示非法（碰撞）"""
    coords = [(0, 0)]
    for d in seq:
        nx = coords[-1][0] + DIRS[d][0]
        ny = coords[-1][1] + DIRS[d][1]
        if (nx, ny) in set(coords):
            return None
        coords.append((nx, ny))
    return coords

def calc_energy(seq, hp_str):
    """计算构型能量（负值越小越好）"""
    coords = decode_coords(seq)
    if coords is None:
        return 0
    coord_set = {c: i for i, c in enumerate(coords)}
    n = len(hp_str)
    energy = 0
    for i in range(n):
        if hp_str[i] != 'H':
            continue
        x, y = coords[i]
        for dx, dy in DIRS:
            nb = (x + dx, y + dy)
            if nb in coord_set:
                j = coord_set[nb]
                if j != i - 1 and j != i + 1 and hp_str[j] == 'H':
                    energy -= 1
    return energy // 2  # 每对计算了两次

def random_seq(n):
    """随机生成合法方向序列（自回避）"""
    for _ in range(10000):
        seq = [random.randint(0, 3) for _ in range(n - 1)]
        if decode_coords(seq) is not None:
            return seq
    return None

def repair_seq(seq):
    """修复不合法的序列：从第一个冲突位置重新随机"""
    result = []
    coords = [(0, 0)]
    coord_set = {(0, 0)}
    for d in seq:
        nx = coords[-1][0] + DIRS[d][0]
        ny = coords[-1][1] + DIRS[d][1]
        if (nx, ny) in coord_set:
            # 尝试随机找一个合法方向
            dirs = list(range(4))
            random.shuffle(dirs)
            placed = False
            for nd in dirs:
                mx = coords[-1][0] + DIRS[nd][0]
                my = coords[-1][1] + DIRS[nd][1]
                if (mx, my) not in coord_set:
                    result.append(nd)
                    coords.append((mx, my))
                    coord_set.add((mx, my))
                    placed = True
                    break
            if not placed:
                # 死路：截断后随机延伸
                remaining = len(seq) - len(result)
                ext = random_seq(remaining + 1)
                if ext:
                    result.extend(ext)
                else:
                    result.extend([random.randint(0, 3)] * remaining)
                break
        else:
            result.append(d)
            coords.append((nx, ny))
            coord_set.add((nx, ny))
    # 补齐长度
    while len(result) < len(seq):
        cx, cy = coords[-1]
        dirs = list(range(4))
        random.shuffle(dirs)
        for nd in dirs:
            nx = cx + DIRS[nd][0]
            ny = cy + DIRS[nd][1]
            if (nx, ny) not in coord_set:
                result.append(nd)
                coords.append((nx, ny))
                coord_set.add((nx, ny))
                break
        else:
            result.append(random.randint(0, 3))
            break
    return result[:len(seq)]

# ─── Pull Move 操作 ────────────────────────────────────────────

def pull_move(seq, hp_str):
    """
    对序列执行一次Pull Move操作
    随机选取一个位置i，尝试将第i个氨基酸拉到相邻格点L，
    并调整i-1或i+1以维持链连通性。
    """
    n = len(seq)
    coords = decode_coords(seq)
    if coords is None:
        return seq[:]

    # 随机选取位置（排除两端）
    idx = random.randint(1, n - 1)
    x, y = coords[idx]
    coord_set = set(coords)

    # 候选目标格点：当前位置的邻居中未被占据的格点
    candidates = []
    for dx, dy in DIRS:
        nx, ny = x + dx, y + dy
        if (nx, ny) not in coord_set or (nx, ny) == coords[idx]:
            # 需要进一步确认移动后与前后氨基酸可连
            prev = coords[idx - 1]
            nxt = coords[idx + 1] if idx < n - 1 else None
            # 新位置 (nx,ny) 必须与 prev 相邻（曼哈顿距离=1）
            if abs(nx - prev[0]) + abs(ny - prev[1]) == 1:
                candidates.append((nx, ny))

    if not candidates:
        return seq[:]

    new_pos = random.choice(candidates)

    # 构造新坐标列表
    new_coords = coords[:]
    new_coords[idx] = new_pos

    # 若与下一个位置断开，需要将 idx+1 拉向 new_pos
    if idx < n - 1:
        nx1, ny1 = new_coords[idx + 1]
        if abs(new_pos[0] - nx1) + abs(new_pos[1] - ny1) != 1:
            # 把 idx+1 移到原来idx的位置（pull）
            old_pos = coords[idx]
            if old_pos not in set(new_coords[:idx + 1]):
                new_coords[idx + 1] = old_pos
            else:
                return seq[:]  # 无法pull，放弃

    # 检查合法性（无碰撞）
    if len(set(new_coords)) != len(new_coords):
        return seq[:]

    # 将坐标转回方向序列
    new_seq = []
    for k in range(len(new_coords) - 1):
        dx = new_coords[k + 1][0] - new_coords[k][0]
        dy = new_coords[k + 1][1] - new_coords[k][1]
        if (dx, dy) in DIRS:
            new_seq.append(DIRS.index((dx, dy)))
        else:
            return seq[:]  # 转换失败
    return new_seq

def apply_pull_moves(seq, hp_str, steps=5):
    """对序列执行多步Pull Move，贪心保留改善的结果"""
    best = seq[:]
    best_e = calc_energy(best, hp_str)
    cur = seq[:]
    cur_e = best_e
    for _ in range(steps):
        new_seq = pull_move(cur, hp_str)
        new_e = calc_energy(new_seq, hp_str)
        if new_e <= cur_e:
            cur = new_seq
            cur_e = new_e
            if cur_e < best_e:
                best = cur[:]
                best_e = cur_e
    return best, best_e

