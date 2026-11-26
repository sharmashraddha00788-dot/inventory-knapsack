# main.py
# Intelligent Inventory Management Using Knapsack Optimization
import csv
import random
import time

from algorithms import fractional_knapsack, knapsack_01_dp

# Sample warehouse inventory (real-life jaisa data)
SAMPLE_ITEMS = [
    {"name": "Laptop",      "weight": 10, "profit": 60},
    {"name": "Mobile",      "weight": 3,  "profit": 40},
    {"name": "Headphones",  "weight": 2,  "profit": 25},
    {"name": "Tablet",      "weight": 5,  "profit": 45},
    {"name": "Smart Watch", "weight": 1,  "profit": 20},
    {"name": "Speaker",     "weight": 6,  "profit": 30},
]


def show_items(items):
    print(f"\n{'No':<4}{'Product':<14}{'Weight':<8}{'Profit':<8}")
    print("-" * 34)
    for i, item in enumerate(items, 1):
        print(f"{i:<4}{item['name']:<14}{item['weight']:<8}{item['profit']:<8}")


def run_both(items, capacity):
    show_items(items)
    print(f"\nStorage Capacity: {capacity}")

    profit_g, sel_g = fractional_knapsack(items, capacity)
    profit_d, sel_d = knapsack_01_dp(items, capacity)

    print("\n--- Greedy (Fractional Knapsack) ---")
    for name, wt, frac in sel_g:
        print(f"  {name}: weight used = {wt}, fraction = {frac}")
    print(f"  Total Profit = {profit_g:.2f}")

    print("\n--- Dynamic Programming (0/1 Knapsack) ---")
    for name, wt, frac in sel_d:
        print(f"  {name}: weight used = {wt}")
    print(f"  Total Profit = {profit_d}")

    print("\nNote: Greedy ka profit DP se zyada ya barabar hota hai,")
    print("kyunki Greedy item ko tod sakta hai, DP nahi.")


def custom_input():
    items = []
    n = int(input("Kitne products hain? "))
    for i in range(n):
        name = input(f"Product {i + 1} ka naam: ")
        weight = int(input("  Weight: "))
        profit = int(input("  Profit: "))
        items.append({"name": name, "weight": weight, "profit": profit})
    capacity = int(input("Storage capacity: "))
    run_both(items, capacity)


def performance_comparison():
    print("\nPerformance comparison (alag-alag size ke inventory pe)")
    sizes = [10, 100, 500, 1000]
    rows = []
    print(f"\n{'Items':<8}{'Greedy time(s)':<18}{'DP time(s)':<16}{'Greedy profit':<16}{'DP profit':<10}")
    print("-" * 68)

    for n in sizes:
        random.seed(n)  # taaki har baar same random data bane
        items = [{"name": f"P{i}", "weight": random.randint(1, 20),
                  "profit": random.randint(10, 100)} for i in range(n)]
        capacity = n * 5

        start = time.perf_counter()
        pg, _ = fractional_knapsack(items, capacity)
        t_greedy = time.perf_counter() - start

        start = time.perf_counter()
        pd, _ = knapsack_01_dp(items, capacity)
        t_dp = time.perf_counter() - start

        print(f"{n:<8}{t_greedy:<18.6f}{t_dp:<16.6f}{pg:<16.2f}{pd:<10}")
        rows.append([n, round(t_greedy, 6), round(t_dp, 6), round(pg, 2), pd])

    # results ko CSV file mein save karo
    with open("results/comparison.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["items", "greedy_time", "dp_time", "greedy_profit", "dp_profit"])
        writer.writerows(rows)
    print("\nResults saved: results/comparison.csv")

    # graph banao (agar matplotlib installed hai)
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        plt.plot([r[0] for r in rows], [r[1] for r in rows], marker="o", label="Greedy")
        plt.plot([r[0] for r in rows], [r[2] for r in rows], marker="o", label="DP")
        plt.xlabel("Number of items")
        plt.ylabel("Time (seconds)")
        plt.title("Greedy vs DP Knapsack")
        plt.legend()
        plt.savefig("results/comparison_graph.png")
        print("Graph saved: results/comparison_graph.png")
    except ImportError:
        print("Graph ke liye: pip install matplotlib")


def main():
    while True:
        print("\n===== Inventory Management (Knapsack) =====")
        print("1. Sample data pe chalao")
        print("2. Apna data daalo")
        print("3. Performance comparison")
        print("4. Exit")
        choice = input("Choice: ")

        if choice == "1":
            run_both(SAMPLE_ITEMS, 15)
        elif choice == "2":
            custom_input()
        elif choice == "3":
            performance_comparison()
        elif choice == "4":
            print("Bye!")
            break
        else:
            print("Galat choice, dobara try karo.")


if __name__ == "__main__":
    main()
