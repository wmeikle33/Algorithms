import math
from typing import List

class SqrtDecomp:
    """
    Range Sum Query (RSQ) with point updates using sqrt decomposition.
    - query(l, r): O(√n)
    - update_set(i, val): O(1) to fix the block sum
    - update_add(i, delta): O(1)
    """
    def __init__(self, arr: List[int]):
        self.n = len(arr)
        self.B = max(1, int(math.sqrt(self.n)))         # block size
        self.arr = list(arr)
        self.num_blocks = (self.n + self.B - 1) // self.B
        self.block_sum = [0] * self.num_blocks
        for i, x in enumerate(self.arr):
            self.block_sum[i // self.B] += x

    def update_set(self, i: int, val: int) -> None:
        """Set arr[i] = val."""
        b = i // self.B
        self.block_sum[b] += val - self.arr[i]
        self.arr[i] = val

    def update_add(self, i: int, delta: int) -> None:
        """Add delta to arr[i]."""
        b = i // self.B
        self.arr[i] += delta
        self.block_sum[b] += delta

    def query(self, l: int, r: int) -> int:
        """Return sum(arr[l:r+1])."""
        if l > r:
            return 0
        res = 0
        start_block = l // self.B
        end_block   = r // self.B
        if start_block == end_block:
            # same block: brute force
            for i in range(l, r + 1):
                res += self.arr[i]
            return res
        # left partial
        end_left = (start_block + 1) * self.B - 1
        for i in range(l, min(end_left, self.n - 1) + 1):
            res += self.arr[i]
        # full blocks
        for b in range(start_block + 1, end_block):
            res += self.block_sum[b]
        # right partial
        start_right = end_block * self.B
        for i in range(start_right, r + 1):
            res += self.arr[i]
        return res
