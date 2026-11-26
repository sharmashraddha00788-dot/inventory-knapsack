# app.py
# Flask backend for the dashboard. Algorithms wahi hain jo algorithms.py mein hain.
import random
import time

from flask import Flask, jsonify, render_template, request

from algorithms import fractional_knapsack, knapsack_01_dp

app = Flask(__name__)


@app.route("/")
def home():
    # dashboard page dikhao
    return render_template("index.html")


@app.route("/api/solve", methods=["POST"])
def solve():
    data = request.get_json()
    capacity = int(data["capacity"])
    items = [{"name": i["name"], "weight": int(i["weight"]), "profit": int(i["profit"])}
             for i in data["items"]]

    # validation: weight 0 ya negative nahi hona chahiye
    if capacity <= 0 or not items or any(i["weight"] <= 0 or i["profit"] < 0 for i in items):
        return jsonify({"error": "Capacity aur weight > 0 hona chahiye, profit >= 0."}), 400

    start = time.perf_counter()
    profit_g, sel_g = fractional_knapsack(items, capacity)
    time_g = time.perf_counter() - start

    start = time.perf_counter()
    profit_d, sel_d = knapsack_01_dp(items, capacity)
    time_d = time.perf_counter() - start

    return jsonify({
        "greedy": {"profit": round(profit_g, 2), "time": time_g,
                   "selected": [{"name": n, "weight": w, "fraction": f} for n, w, f in sel_g]},
        "dp": {"profit": profit_d, "time": time_d,
               "selected": [{"name": n, "weight": w, "fraction": f} for n, w, f in sel_d]},
    })


@app.route("/api/performance")
def performance():
    rows = []
    for n in [10, 100, 500, 1000]:
        random.seed(n)
        items = [{"name": f"P{i}", "weight": random.randint(1, 20),
                  "profit": random.randint(10, 100)} for i in range(n)]
        capacity = n * 5

        start = time.perf_counter()
        pg, _ = fractional_knapsack(items, capacity)
        tg = time.perf_counter() - start

        start = time.perf_counter()
        pd, _ = knapsack_01_dp(items, capacity)
        td = time.perf_counter() - start

        rows.append({"items": n, "greedy_time": tg, "dp_time": td,
                     "greedy_profit": round(pg, 2), "dp_profit": pd})
    return jsonify(rows)


if __name__ == "__main__":
    app.run(debug=True)
