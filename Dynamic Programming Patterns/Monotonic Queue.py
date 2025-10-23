from collections import deque
from typing import List

def constrained_subseq_sum(a: List[int], K: int) -> int:
    n = len(a)
    dp = [0]*n
    dq = deque() 

    for i in range(n):
        best = dp[dq[0]] if dq else 0
        dp[i] = a[i] + max(0, best)

        while dq and dp[dq[-1]] <= dp[i]:
            dq.pop()
        dq.append(i)

        while dq and dq[0] < i - K + 1:
            dq.popleft()

    return max(dp)
