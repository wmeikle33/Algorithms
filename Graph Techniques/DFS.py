from math import inf
from typing import List

def coin_change_min(coins: List[int], amount: int) -> int:
    dp = [0] + [inf] * amount   # dp[x] = min coins to make x
    for x in range(1, amount + 1):
        for c in coins:
            if x - c >= 0 and dp[x - c] != inf:
                dp[x] = min(dp[x], dp[x - c] + 1)
    return -1 if dp[amount] == inf else dp[amount]
