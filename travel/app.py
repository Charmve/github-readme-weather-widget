from flask import Flask, render_template, request
import itertools

app = Flask(__name__)

# 城市和线路数据
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


def tsp(start, visited_cities):
    n = len(visited_cities)
    mask = 0
    for city in visited_cities:
        mask |= (1 << visited_cities.index(city))

    # 动态规划表: dp[mask][i] 表示到达状态 mask 的最小费用，最后在城市 i 停止
    dp = [[float('inf')] * n for _ in range(1 << n)]
    path = [[-1] * n for _ in range(1 << n)]  # 记录路径
    dp[1 << start][start] = 0  # 起点城市的状态

    for mask in range(1 << n):
        for u in range(n):
            if dp[mask][u] == float('inf'):
                continue
            for v in range(n):
                if (mask & (1 << v)) == 0 and v in visited_cities:  # 如果城市 v 没有被访问
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
        route.append(visited_cities[last_city])
        next_city = path[mask][last_city]
        mask ^= (1 << last_city)  # 去掉 last_city
        last_city = next_city

    route.append(visited_cities[start])  # 添加起点城市
    route.reverse()  # 反转路径

    return min_cost, route

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form.get('cities')  # 获取输入的城市
        selected_cities = [city.strip() for city in user_input.split(',') if city.strip()]  # 处理用户输入
        start_city = "苏州"
        
        if start_city not in selected_cities:
            selected_cities.insert(0, start_city)  # 添加苏州为起点
        
        start_city_index = selected_cities.index(start_city)


        # 创建一个距离矩阵
        n = len(selected_cities)
        global distance_matrix
        distance_matrix = [[0] * n for _ in range(n)]

        for (city1, city2), cost in lines.items():
            i = selected_cities.index(city1)
            j = selected_cities.index(city2)
            distance_matrix[i][j] = cost
            distance_matrix[j][i] = cost  # 无向图

        min_cost, route = tsp(start_city_index, selected_cities)  # 计算 TSP
        return render_template('result.html', cost=min_cost, route=route)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
