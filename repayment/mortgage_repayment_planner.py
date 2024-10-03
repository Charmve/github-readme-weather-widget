from flask import Flask, render_template, request
import random
from datetime import datetime
from pyecharts import options as opts
from pyecharts.charts import Line

app = Flask(__name__)

def random_repayment_high():
    return random.choice([True, False])

def random_repayment_day():
    return random.randint(1, 30)

def get_next_payment_date(current_date):
    year = current_date.year
    month = current_date.month + 1
    if month > 12:
        month = 1
        year += 1    
    return datetime(year, month, 21)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        principal = float(request.form['principal'])
        annual_interest_rate = float(request.form['annual_interest_rate'])
        monthly_income = float(request.form['monthly_income'])
        monthly_expenses = float(request.form['monthly_expenses'])

        monthly_interest_rate = annual_interest_rate / 12
        total_months = 144  # 假设贷款期限为12年（144个月）
        monthly_principal_payment = principal / total_months
        
        repayments = []  # 存储还款信息
        remaining_balance = principal
        payment_dates = []
        payment_amounts = []
        principal_payments = []
        interest_payments = []

        net_monthly_cash_flow = monthly_income - monthly_expenses
        current_date = datetime.now()  # 从当前日期开始
        while remaining_balance > 0:
            interest_for_the_month = remaining_balance * monthly_interest_rate
            total_monthly_payment = monthly_principal_payment + interest_for_the_month
            
            payment = total_monthly_payment if random_repayment_high() else max(total_monthly_payment, net_monthly_cash_flow)
            
            principal_payment = payment - interest_for_the_month
            remaining_balance -= principal_payment
            
            repayments.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'repayment_amount': payment,
                'principal_payment': principal_payment,
                'interest_payment': interest_for_the_month,
                'remaining_balance': max(remaining_balance, 0)
            })

            # 收集数据用于绘图
            payment_dates.append(current_date.strftime('%Y-%m-%d'))
            payment_amounts.append(payment)
            principal_payments.append(principal_payment)
            interest_payments.append(interest_for_the_month)

            current_date = get_next_payment_date(current_date)

        # 绘制图表
        line_chart = (
            Line()
            .add_xaxis(payment_dates)
            .add_yaxis("每月还款", payment_amounts)
            .add_yaxis("本金还款", principal_payments)
            .add_yaxis("利息还款", interest_payments)
            .set_global_opts(title_opts=opts.TitleOpts(title="贷款还款计划"),
                             xaxis_opts=opts.AxisOpts(name="日期"),
                             yaxis_opts=opts.AxisOpts(name="金额"))
        )

        # 渲染图表
        chart_html = line_chart.dump_options_with_quotes()

        return render_template('result.html', repayments=repayments, chart_html=chart_html)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)