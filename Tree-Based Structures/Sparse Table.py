from math import log2, floor
from typing import List, Tuple

class SparseTableArgmin:
    __slots__ = ("n","K","st","lg")

    def __init__(self, a: List[int]):
        self.n = len(a)
        self.K = floor(log2(self.n)) + 1 if self.n else 1
        self.lg = [0] * (self.n + 1)
        for i in range(2, self.n + 1):
            self.lg[i] = self.lg[i // 2] + 1

        self.st = [[(a[i], i) for i in range(self.n)]]
        k = 1
        while (1 << k) <= self.n:
            prev = self.st[k-1]
            cur_len = self.n - (1 << k) + 1
            cur = [None] * cur_len
            half = 1 << (k - 1)
            for i in range(cur_len):
                left = prev[i]
                right = prev[i + half]
                cur[i] = left if (left[0] < right[0] or (left[0] == right[0] and left[1] < right[1])) else right
            self.st.append(cur)
            k += 1

    def query(self, l: int, r: int) -> Tuple[int,int]:
        k = self.lg[r - l + 1]
        left = self.st[k][l]
        right = self.st[k][r - (1 << k) + 1]
        return left if (left[0] < right[0] or (left[0] == right[0] and left[1] < right[1])) else right
