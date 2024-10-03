import numpy as np
from datetime import datetime, timedelta
import matplotlib as mpl
import matplotlib.pyplot as plt
import random

import pyecharts.options as opts
from pyecharts.charts import Line


# 指定默认字体
mpl.rcParams["font.sans-serif"] = ["SimHei"]  # 指定默认字体为黑体
mpl.rcParams["axes.unicode_minus"] = False  # 解决保存图像时负号'-'显示为方块的问题
plt.rcParams["font.family"] = "SimHei"

def random_repayment_high():
    is_repayment = False
    # 随机选择生成偶数或奇数
    if random.random() < 0.5:
        # 生成偶数
        number = random.randint(0, 100) * 2  # 随机生成范围在0到100的偶数
    else:
        # 生成奇数
        number = random.randint(0, 100) * 2 + 1  # 随机生成范围在0到99的奇数
    
    is_repayment = True if number % 2 else False
    return is_repayment


def random_repayment_day():
    # 随机选择生成偶数或奇数
    if random.random() < 0.5:
        # 生成偶数：假设范围是 0 到 60（共 30 个偶数）
        number = random.choice([i for i in range(1, 31, 2)])  # 生成0到60之间的偶数
    else:
        # 生成奇数：假设范围是 1 到 59（共 30 个奇数）
        number = random.choice([i for i in range(1, 31, 2)])  # 生成1到59之间的奇数
    return number


def generate_number():
    # 随机生成 0 到 30 之间的数
    number = random.randint(1, 31)  # 包含1和31
    return number

# 函数: 检查日期是否为工作日
def is_weekday(date):
    return date.weekday() < 5  # 周一到周五为工作日

# 函数: 获取下一个工作日
def get_next_business_day(start_date):
    next_day = start_date + timedelta(days=1)
    while not is_weekday(next_day):
        next_day += timedelta(days=1)
    return next_day

# 函数: 生成下一个还款日期（每月21号）
def get_next_payment_date(current_date):
    year = current_date.year
    month = current_date.month

    month += 1
    if month > 12:
        month = 1
        year += 1    
    
    next_payment_date = datetime(year, month, 21)
    return next_payment_date

total_interest_ = 320422.43
greater_repayment_schedule_ = []
total_repayment_ = 0.00

# 参数设置
principal = 1220000  # 总贷款金额
annual_interest_rate = 0.0285  # 年利率
monthly_interest_rate = annual_interest_rate / 12
loan_start_date = '2024-06-21'

# 已还款信息
repayments = [
    {'date': '2024-07-21', 'amount': 10013.35, 'principal_payment': 7115.85, 'interest_for_the_month': 2897.5},
    {'date': '2024-08-08', 'amount': 150000.00, 'principal_payment': 148271.64, 'interest_for_the_month': 1728.36},
    {'date': '2024-08-21', 'amount': 8580.56, 'principal_payment': 7484.9, 'interest_for_the_month': 1095.66},
    {'date': '2024-08-28', 'amount': 22450.00, 'principal_payment': 21864.17, 'interest_for_the_month': 585.83}
]
# 每月收入与支出
monthly_income = 31000
monthly_expenses = 7000
net_monthly_cash_flow = monthly_income - monthly_expenses
# 计算每期需还的本金
total_months = 144  # 假设贷款期限为12年（144个月）
monthly_principal_payment = principal / total_months

for i in range(100):
    
    remaining_balance = principal

    # 记录每期还款情况
    total_repayment = sum(r['amount'] for r in repayments)
    repayment_schedule = []

    # 处理已还款
    for repayment in repayments:
        repayment_amount = repayment['amount']
        repayment_date = repayment['date']

        remaining_balance -= repayment_amount
        total_repayment += repayment_amount

        repayment_schedule.append({
            'date': repayment_date,
            'repayment_amount': repayment_amount,
            'principal_payment': repayment['principal_payment'],
            'interest_payment': repayment['interest_for_the_month'],
            'remaining_balance': max(remaining_balance, 0)
        })

    # 开始每月的还款过程
    current_date = datetime.strptime(repayments[-1]['date'], '%Y-%m-%d')  # 从最后一次还款开始
    print("最近一次还款: ", current_date)
    while remaining_balance > 0:
        interest_for_the_month = remaining_balance * monthly_interest_rate
        total_monthly_payment = monthly_principal_payment + interest_for_the_month

        # 检查可用现金流
        if random_repayment_high():
            payment = max(total_monthly_payment, net_monthly_cash_flow)
        else:
            payment = total_monthly_payment
        
        if random_repayment_high():
            payment = net_monthly_cash_flow

            random_day = random_repayment_day()
            if random_day not in range(1, 31):
                random_day = random_repayment_day()
            
            try:
                repayment_date = datetime(current_date.year, current_date.month, random_day)
            except:
                continue
            current_date = repayment_date if repayment_date > current_date else current_date

            # 更新每月随机还款后剩余本金
            principal_payment = payment - interest_for_the_month  # 本金还款
            remaining_balance -= principal_payment
            total_repayment += payment

            repayment_schedule.append({
                'date': repayment_date.strftime('%Y-%m-%d'),
                'repayment_amount': payment,
                'principal_payment': principal_payment,
                'interest_payment': interest_for_the_month,
                'remaining_balance': max(remaining_balance, 0)
            })

        # 更新每月固定还款后剩余本金
        principal_payment = payment - interest_for_the_month  # 本金还款
        remaining_balance -= principal_payment
        total_repayment += payment

        # 记录新的还款情况
        current_date = get_next_payment_date(current_date)  # 获取下一个还款日期
        # print("下一个还款日期: ", current_date)
        # repayment_date = get_next_business_day(current_date)  # 确保后续日期为工作日
        repayment_schedule.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'repayment_amount': payment,
            'principal_payment': principal_payment,
            'interest_payment': interest_for_the_month,
            'remaining_balance': max(remaining_balance, 0)
        })
    
    total_interest = (total_repayment-principal)
    
    # 输出还款情况
    print("详细还款计划:")
    print(f"{'日期':<15} {'还款金额':<15} {'本金还款':<15} {'利息还款':<15} {'剩余本金'}")
    for entry in repayment_schedule:
        print(f"{entry['date']:<15} {entry['repayment_amount']:<15.2f} {entry['principal_payment']:<15.2f} {entry['interest_payment']:<15.2f} {entry['remaining_balance']:.2f}")

    print(f"\n{i} - 总还款期数: {len(repayment_schedule)}  贷款金额: {principal}  总还款金额: {total_repayment:.2f}  总还款利息: {total_interest:.2f}")
    
    if  total_interest <= total_interest_:
        total_interest_ = total_interest
        greater_repayment_schedule_ = repayment_schedule
        total_repayment_ = total_repayment

print("\n\n最优还款计划:")
for entry in greater_repayment_schedule_:
    print(f"{entry['date']:<15} {entry['repayment_amount']:<15.2f} {entry['principal_payment']:<15.2f} {entry['interest_payment']:<15.2f} {entry['remaining_balance']:.2f}")
print(f"\n总还款期数: {len(greater_repayment_schedule_)}  贷款金额: {principal}  总还款金额: {total_repayment_:.2f}  总还款利息: {total_repayment_:.2f}")


# 准备数据用于可视化
dates = [entry['date'] for entry in greater_repayment_schedule_]
principal_payments = [entry['principal_payment'] for entry in greater_repayment_schedule_]
interest_payments = [entry['interest_payment'] for entry in greater_repayment_schedule_]
remaining_balances = [entry['remaining_balance'] for entry in greater_repayment_schedule_]

if False:

    # 使用pyecharts绘图
    line_chart = (
        Line()
        .add_xaxis(dates)
        .add_yaxis("本金还款", principal_payments, is_smooth=True)
        .add_yaxis("利息还款", interest_payments, is_smooth=True, color="orange")
        .add_yaxis("剩余本金", remaining_balances, is_smooth=True, color="green")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="还款计划"),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            xaxis_opts=opts.AxisOpts(name="日期", type_="category"),
            yaxis_opts=opts.AxisOpts(name="金额（元）"),
            datazoom_opts=opts.DataZoomOpts(),
        )
    )

    # 渲染到本地html文件
    line_chart.render("repayment_schedule.html")
else:
    

    # 创建图形
    plt.figure(figsize=(12, 6))

    # 本金还款
    plt.subplot(3, 1, 1)
    plt.plot(dates, principal_payments, label='本金还款', marker='o')
    plt.title('每期本金还款')
    plt.xticks(rotation=45)
    plt.ylabel('金额（元）')
    plt.grid()

    # 利息还款
    plt.subplot(3, 1, 2)
    plt.plot(dates, interest_payments, label='利息还款', color='orange', marker='o')
    plt.title('每期利息还款')
    plt.xticks(rotation=45)
    plt.ylabel('金额（元）')
    plt.grid()

    # 剩余本金
    plt.subplot(3, 1, 3)
    plt.plot(dates, remaining_balances, label='剩余本金', color='green', marker='o')
    plt.title('剩余本金变化')
    plt.xticks(rotation=45)
    plt.ylabel('金额（元）')
    plt.grid()

    plt.tight_layout()
    plt.show()
