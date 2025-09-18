from typing import List, Optional, Tuple

def apply_range_adds(n: int, updates: List[Tuple[int,int,int]], base: Optional[List[int]] = None) -> List[int]:
    arr = [0]*n if base is None else base[:]
    diff = [0]*(n+1)
    for l, r, d in updates:
        diff[l] += d
        if r + 1 <= n - 1:
            diff[r + 1] -= d

    run = 0
    for i in range(n):
        run += diff[i]
        arr[i] += run
    return arr
