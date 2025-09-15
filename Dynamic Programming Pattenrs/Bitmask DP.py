from math import inf

def tsp_min_cycle(cost):
    n = len(cost)
    N = 1 << n
    # dp[mask][i] = min cost to reach set 'mask' and end at node i
    dp = [[inf] * n for _ in range(N)]
    dp[1 << 0][0] = 0  # start at node 0, mask has only 0

    for mask in range(N):
        if not (mask & 1):  # ensure tours start from node 0 (optional pruning)
            continue
        for i in range(n):
            if not (mask & (1 << i)):
                continue
            cur = dp[mask][i]
            if cur == inf:
                continue
            # try to go to j not yet in mask
            remaining = (~mask) & (N - 1)
            j = remaining
            while j:
                lsb = j & -j
                v = (lsb.bit_length() - 1)
                nxt = mask | (1 << v)
                dp[nxt][v] = min(dp[nxt][v], cur + cost[i][v])
                j -= lsb

    full = N - 1
    ans = min(dp[full][i] + cost[i][0] for i in range(n))
    return ans
