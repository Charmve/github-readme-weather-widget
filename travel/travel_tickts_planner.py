import itertools

# 城市和线路数据
cities = ["苏州", "青岛", "日照", "威海", "烟台"]
lines = {
    ("苏州", "青岛"): 276,
    ("苏州", "日照"): 247,
    ("苏州", "威海"): 376,
    ("苏州", "烟台"): 358,

    ("青岛", "日照"): 57,
    ("青岛", "威海"): 97,
    ("青岛", "烟台"): 68,
    ("青岛", "苏州"): 289,

    ("日照", "威海"): 133,
    ("日照", "烟台"): 117,
    ("日照", "青岛"): 57,
    ("日照", "苏州"): 225,

    ("威海", "苏州"): 351,
    ("威海", "烟台"): 22,
    ("威海", "青岛"): 93,
    ("威海", "日照"): 126,

    ("烟台", "威海"): 25,
    ("烟台", "日照"): 122,
    ("烟台", "青岛"): 93,
    ("烟台", "苏州"): 297,
}

# 创建一个距离矩阵
n = len(cities)
distance_matrix = [[0] * n for _ in range(n)]

for (city1, city2), cost in lines.items():
    i = cities.index(city1)
    j = cities.index(city2)
    distance_matrix[i][j] = cost
    distance_matrix[j][i] = cost  # 无向图

def tsp(start):
    # 动态规划表: dp[mask][i] 表示到达状态 mask 的最小费用，最后在城市 i 停止
    dp = [[float('inf')] * n for _ in range(1 << n)]
    path = [[-1] * n for _ in range(1 << n)]  # 记录路径
    dp[1][start] = 0  # 起点城市的状态

    for mask in range(1 << n):
        for u in range(n):
            if dp[mask][u] == float('inf'):
                continue
            for v in range(n):
                if mask & (1 << v) == 0:  # 如果城市 v 没有被访问
                    new_mask = mask | (1 << v)
                    if dp[new_mask][v] > dp[mask][u] + distance_matrix[u][v]:
                        dp[new_mask][v] = dp[mask][u] + distance_matrix[u][v]
                        path[new_mask][v] = u  # 记录从哪个城市到达

    # 找到回到起点的最小费用
    min_cost = float('inf')
    final_mask = (1 << n) - 1  # 所有城市都已访问
    last_city = -1
    
    for u in range(n):
        if dp[final_mask][u] < float('inf'):
            cost = dp[final_mask][u] + distance_matrix[u][start]
            if cost < min_cost:
                min_cost = cost
                last_city = u

    # 重建路径
    route = []
    mask = final_mask

    while last_city != -1:
        route.append(cities[last_city])
        next_city = path[mask][last_city]
        mask ^= (1 << last_city)  # 去掉 last_city
        last_city = next_city

    route.append(cities[start])  # 添加起点城市
    route.reverse()  # 反转路径

    return min_cost, route

# 从苏州出发的最小费用
start_city_index = cities.index("苏州")
min_cost, route = tsp(start_city_index)

print("从苏州出发，走遍所有城市的最小费用为: {}".format(min_cost))
print("具体路线为: {}".format(" -> ".join(route)))