from flask import Flask, render_template, request, session, redirect, url_for
import pandas as pd
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

session_data = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    trades = []
    if request.method == 'POST':
        starting_balance = float(request.form['starting_balance'])
        target_balance = float(request.form['target_balance'])
        stop_loss_pips = float(request.form['stop_loss'])
        pip_value = float(request.form['pip_value'])
        reward_ratio = float(request.form['reward_ratio'])

        balance = starting_balance
        trade_num = 0

        while balance < target_balance:
            trade_num += 1
            risk_pct = 0.01  # default 1% risk
            risk_amount = balance * risk_pct
            profit = risk_amount * reward_ratio
            lot_size = round(risk_amount / (stop_loss_pips * pip_value), 2)

            trades.append({
                "Trade #": trade_num,
                "Balance": f"${balance:.2f}",
                "Profit": f"${profit:.2f}",
                "Risk %": f"{risk_pct * 100:.2f}%",
                "Lot Size": lot_size
            })
            balance += profit

    return render_template('calculator.html', trades=trades)

if __name__ == '__main__':
    app.run(debug=True)
