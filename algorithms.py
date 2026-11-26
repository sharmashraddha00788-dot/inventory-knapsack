# algorithms.py
# Is file mein dono knapsack algorithms hain.
# Har item ek dictionary hai: {"name": ..., "weight": ..., "profit": ...}


def fractional_knapsack(items, capacity):
    """GREEDY approach: item ka hissa (fraction) bhi le sakte hain."""
    # Step 1: har item ka profit/weight ratio nikalo
    ratio_list = []
    for item in items:
        ratio = item["profit"] / item["weight"]
        ratio_list.append((ratio, item))

    # Step 2: ratio ke hisaab se bade se chhota sort karo
    ratio_list.sort(key=lambda pair: pair[0], reverse=True)

    total_profit = 0
    remaining = capacity
    selected = []

    # Step 3: jo best ratio wala hai pehle bharo
    for ratio, item in ratio_list:
        if remaining == 0:
            break
        if item["weight"] <= remaining:
            # poora item aa sakta hai
            remaining -= item["weight"]
            total_profit += item["profit"]
            selected.append((item["name"], item["weight"], 1.0))
        else:
            # sirf thoda sa hissa aa sakta hai
            fraction = remaining / item["weight"]
            total_profit += item["profit"] * fraction
            selected.append((item["name"], remaining, round(fraction, 2)))
            remaining = 0

    return total_profit, selected


def knapsack_01_dp(items, capacity):
    """DYNAMIC PROGRAMMING approach: item ya to poora lo ya bilkul nahi (0/1)."""
    n = len(items)

    # Step 1: table banao. dp[i][w] = pehle i items aur w capacity mein max profit
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    # Step 2: table bharo
    for i in range(1, n + 1):
        weight = items[i - 1]["weight"]
        profit = items[i - 1]["profit"]
        for w in range(capacity + 1):
            # option 1: is item ko mat lo
            dp[i][w] = dp[i - 1][w]
            # option 2: lo (agar jagah hai) aur dekho profit zyada hai ya nahi
            if weight <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - weight] + profit)

    # Step 3: peeche se chalke pata lagao kaunse items liye the
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:  # matlab item i liya gaya tha
            item = items[i - 1]
            selected.append((item["name"], item["weight"], 1.0))
            w -= item["weight"]
    selected.reverse()

    return dp[n][capacity], selected
