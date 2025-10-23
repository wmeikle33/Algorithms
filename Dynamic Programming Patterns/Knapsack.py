def knapsack_01(items: List[Item], W: int) -> int:
    dp = [0]*(W+1)
    for w, v in items:
        for c in range(W, w-1, -1):
            dp[c] = max(dp[c], dp[c-w] + v)
    return dp[W]
