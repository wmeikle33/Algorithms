from typing import List, Optional, Tuple

def apply_range_adds(n: int, updates: List[Tuple[int,int,int]], base: Optional[List[int]] = None) -> List[int]:
    """
    n: length of array (0-indexed)
    updates: list of (l, r, delta) meaning a[l..r] += delta
    base: optional starting array (length n); default zeros
    """
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

# Example
n = 10
updates = [(2, 5, 3), (0, 3, -2), (7, 9, 4)]
print(apply_range_adds(n, updates))  # final array after all updates
