
class SegTreeSum:
    __slots__ = ("n", "size", "tree")

    def __init__(self, a: List[int]):
        self.n = len(a)
        self.size = 1 << (self.n - 1).bit_length() 
        self.tree = [0] * (2 * self.size)
        self.tree[self.size:self.size + self.n] = a
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    def set(self, i: int, v: int) -> None:
        p = i + self.size
        self.tree[p] = v
        p //= 2
        while p:
            self.tree[p] = self.tree[2 * p] + self.tree[2 * p + 1]
            p //= 2

    def add(self, i: int, delta: int) -> None:
        p = i + self.size
        self.tree[p] += delta
        p //= 2
        while p:
            self.tree[p] = self.tree[2 * p] + self.tree[2 * p + 1]
            p //= 2

    def sum(self, l: int, r: int) -> int:
        l += self.size; r += self.size
        res = 0
        while l < r:
            if l & 1:
                res += self.tree[l]; l += 1
            if r & 1:
                r -= 1; res += self.tree[r]
            l //= 2; r //= 2
        return res
