import secrets

MASK64 = (1 << 64) - 1

class RandomizedStringHasher:
    """
    Rolling hash with TWO independent moduli:
      - 64-bit wraparound (mod 2^64)
      - Large prime 1_000_000_007
    Bases are chosen at random each run.
    """
    def __init__(self, s: str):
        self.s = s
        self.n = len(s)
        # random bases (≥ 256 so characters don't dominate)
        self.b1 = secrets.randbelow(1_000_000_000 - 256) + 256
        self.b2 = secrets.randbelow(1_000_000_000 - 256) + 256
        self.M2 = 1_000_000_007

        # precompute powers and prefixes for both moduli
        self.pw1 = [1] * (self.n + 1)   # 64-bit
        self.pw2 = [1] * (self.n + 1)   # mod M2
        self.ph1 = [0] * (self.n + 1)
        self.ph2 = [0] * (self.n + 1)

        for i, ch in enumerate(s, 1):
            c = ord(ch)
            # 64-bit (implicit mod by masking)
            self.pw1[i] = (self.pw1[i-1] * self.b1) & MASK64
            self.ph1[i] = ((self.ph1[i-1] * self.b1) + c) & MASK64
            # mod prime
            self.pw2[i] = (self.pw2[i-1] * self.b2) % self.M2
            self.ph2[i] = (self.ph2[i-1] * self.b2 + c) % self.M2

    def hash(self, l: int, r: int):
        """
        Return a pair of hashes for substring s[l:r] (0 <= l <= r <= n).
        """
        # 64-bit
        x1 = (self.ph1[r] - (self.ph1[l] * self.pw1[r - l] & MASK64)) & MASK64
        # mod prime
        x2 = (self.ph2[r] - (self.ph2[l] * self.pw2[r - l])) % self.M2
        return (x1, x2)

    def equal(self, l1: int, r1: int, l2: int, r2: int) -> bool:
        """
        O(1) substring equality test using randomized double hashing.
        """
        return self.hash(l1, r1) == self.hash(l2, r2)
