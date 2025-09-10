from math import log2, gcd
from typing import Callable, List

class SparseTable:
    """
    Works for idempotent + associative ops like min/max/gcd.
    Query is inclusive: query(l, r), 0 <= l <= r < n
    """
    def __init__(self, a: List[int], op: Callable[[int, int], int]):
        self.a = a
        self.n = len(a)
        self.op = op
        self.K = (self.n.bit_length())  # floor(log2(n)) + 1
        # precompute logs: lg[x] = floor(log2(x))
        self.lg = [0] * (self.n + 1)
        for i in range(2, self.n + 1):
            self.lg[i] = self.lg[i // 2] + 1

        # build st[k][i] for length 2^k starting at i
        self.st = [self.a[:] ]  # k = 0
        k = 1
        while (1 << k) <= self.n:
            prev = self.st[k - 1]
            size = 1 << k
            half = size >> 1
            row = [0] * (self.n - size + 1)
            for i in range(self.n - size + 1):
                row[i] = self.op(prev[i], prev[i + half])
            self.st.append(row)
            k += 1

    def query(self, l: int, r: int) -> int:
        """Return op over a[l..r] inclusive in O(1)."""
        k = self.lg[r - l + 1]
        left = self.st[k][l]
        right = self.st[k][r - (1 << k) + 1]
        return self.op(left, right)

# Convenience builders
def MinSparseTable(a: List[int]) -> SparseTable:
    return SparseTable(a, min)

def MaxSparseTable(a: List[int]) -> SparseTable:
    return SparseTable(a, max)

def GcdSparseTable(a: List[int]) -> SparseTable:
    return SparseTable(a, gcd)
