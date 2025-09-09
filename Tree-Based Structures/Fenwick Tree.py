class Fenwick:
    def __init__(self, n: int):
        self.n = n
        self.bit = [0] * (n + 1)  

    def add(self, i: int, delta: int) -> None:
        while i <= self.n:
            self.bit[i] += delta
            i += i & -i

    def sum(self, i: int) -> int:
        s = 0
        while i > 0:
            s += self.bit[i]
            i &= i - 1
        return s
