INF = 10**15
n = 100
dp = [INF] * (n + 1)
dp[0] = 0  # base
for i in range(1, n + 1):
    # dp[i] = min/max over previous states
    pass

# 2D example
m, n = 10, 10
dp = [[0] * (n + 1) for _ in range(m + 1)]
# fill base rows/cols, then iterate
for i in range(1, m + 1):
    for j in range(1, n + 1):
        # dp[i][j] from dp[i-1][*], dp[*][j-1], etc.
        pass
