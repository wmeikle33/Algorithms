import secrets

MASK64 = (1 << 64) - 1

class RandomizedStringHasher:
    def __init__(self, s: str):
        self.s = s
        self.n = len(s)
        self.b1 = secrets.randbelow(1_000_000_000 - 256) + 256
        self.b2 = secrets.randbelow(1_000_000_000 - 256) + 256
        self.M2 = 1_000_000_007

        self.pw1 = [1] * (self.n + 1)   # 64-bit
        self.pw2 = [1] * (self.n + 1)   # mod M2
        self.ph1 = [0] * (self.n + 1)
        self.ph2 = [0] * (self.n + 1)

        for i, ch in enumerate(s, 1):
            c = ord(ch)
            self.pw1[i] = (self.pw1[i-1] * self.b1) & MASK64
            self.ph1[i] = ((self.ph1[i-1] * self.b1) + c) & MASK64
            self.pw2[i] = (self.pw2[i-1] * self.b2) % self.M2
            self.ph2[i] = (self.ph2[i-1] * self.b2 + c) % self.M2

    def hash(self, l: int, r: int):
        x1 = (self.ph1[r] - (self.ph1[l] * self.pw1[r - l] & MASK64)) & MASK64
        x2 = (self.ph2[r] - (self.ph2[l] * self.pw2[r - l])) % self.M2
        return (x1, x2)

    def equal(self, l1: int, r1: int, l2: int, r2: int) -> bool:
        return self.hash(l1, r1) == self.hash(l2, r2)
