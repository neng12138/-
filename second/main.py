import random
# 城市之间的距离， 起点和终点的是a （a,b,c,d）
D = [ [0,1,0.5,1],[1,0,1,1],[1.5,5,0,1],[1,1,1,0] ]

def get_distance(first_index, last_index):
    """获取两个城市之间的距离"""
    return D[first_index][last_index]

def get_sum_distance(d:list[float]):
    """获取当前路径下的总距离"""
    sum_distance = 0
    for index in range(len(d)-1):
        sum_distance += get_distance(d[index], d[(index+1)])
    return sum_distance + get_distance(d[-1],0)

# 0-a 1-b 2-c 3-d
def get_another_d(d:list[float]):
    """获取一个新的邻域"""
    first_num = random.randint(1,3)
    second_num = random.randint(1,3)
    flag = True
    if is_taboo(first_num, second_num):  # 判断是否在禁忌表中
        flag = False
    else:
        add_taboo(first_num, second_num)    # 添加到禁忌表中
    new_d = d.copy()    # 数据复制
    f = new_d[first_num]
    new_d[first_num] = new_d[second_num]
    new_d[second_num] = f
    return new_d,flag,get_sum_distance(new_d)

# 0-a 1-b 2-c 3-d
def print_d(d:list[str]):
    """打印当前的路径"""
    for item in d:
        if item != d[-1]:
            print(f"{item} -> ", end='')
            continue
        print(f"{item} -> a")

# 0-a 1-b 2-c 3-d
def interpret_d(d:list[float]):
    """显示路径，并将路径打印"""
    new_d = []
    for item in d:
        if item == 0:
            new_d.append('a')
        elif item == 1:
            new_d.append('b')
        elif item == 2:
            new_d.append('c')
        else:
            new_d.append('d')
    print_d(new_d)


taboo_list = []   # 禁忌表（len=4）
def add_taboo(first_index, second_index):
    """添加到禁忌表中"""
    if len(taboo_list) >= 4:
        taboo_list.pop(0)   # 移除第一个元素
    taboo_list.append((first_index, second_index))  # 元组（两个索引）
def is_taboo(first_index, second_index):
    """判断是否在禁忌表中"""
    if (first_index, second_index) in taboo_list or (second_index, first_index) in taboo_list:
        return True
    return False


# 0-a 1-b 2-c 3-d
def main(range_num:int=10000, max_close_num:int=50):
    """主函数"""
    d = [0 , 1 ,2 , 3]   # a -> b -> c -> d -> a   （初始解）
    best_d = d.copy()   # 数据复制
    best_d_distance = get_sum_distance(best_d)
    close_num = 0
    max_close_num = max_close_num     # 可接受的最大关闭次数
    work_num = 0    # 迭代步数
    for _ in range(range_num):
        new_d, flag, new_distance = get_another_d(d)    # 随机生成一个新的邻域解
        if (not flag) and len(taboo_list) < 4:     # 在禁忌表中且当前禁忌表未满
            continue
        if (not flag) and new_distance >= best_d_distance:     # 在禁忌表中且当前路径更差
            continue
        work_num += 1   # 迭代步数
        if new_distance < best_d_distance:
            # 当前路径好，则接受此路径
            best_d = new_d.copy()   # 数据复制
            best_d_distance = get_sum_distance(best_d)
            d = new_d
            close_num -= 10     # 找到一个更好的解
        else:       # 找不到更好的解
            if random.random() < 0.4:   # 40%的概率接受新解
                d = new_d
            close_num += 2

        # 很长时间内找不到更好的解
        if close_num > max_close_num:
            break
        

    print("="*50)
    print(f"初始的路径是: a -> b -> c -> d -> a")
    print(f"最好的路径是: ", end='')
    interpret_d(best_d)
    print(f"最好的路径下的总距离是: {best_d_distance}")
    print(f"迭代步数： {work_num}")
    print("="*50)

# 运行主函数
if __name__ == '__main__':
    main()
   
