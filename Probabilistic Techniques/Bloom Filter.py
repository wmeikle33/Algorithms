import math, hashlib
from typing import Iterable

def _to_bytes(x) -> bytes:
    if isinstance(x, bytes):
        return x
    if isinstance(x, str):
        return x.encode("utf-8")
    return str(x).encode("utf-8")

def _calc_m_k(n: int, p: float) -> tuple[int, int]:
    """
    Given expected items n and desired false-positive prob p (0 < p < 1),
    return optimal bit-array size m and number of hash functions k.
    m = ceil(-n * ln p / (ln 2)^2)
    k = round((m / n) * ln 2)
    """
    m = math.ceil(-n * math.log(p) / (math.log(2) ** 2))
    k = max(1, round((m / n) * math.log(2)))
    return m, k

class BloomFilter:
    def __init__(self, m: int, k: int):
        self.m = m                      # number of bits
        self.k = k                      # number of hash functions
        self.bits = bytearray((m + 7) // 8)
        self.count = 0                  # items inserted (not distinct)

    @classmethod
    def from_params(cls, n: int, p: float = 0.01) -> "BloomFilter":
        m, k = _calc_m_k(n, p)
        return cls(m, k)

    # ----- bit operations -----
    def _setbit(self, i: int) -> None:
        self.bits[i >> 3] |= 1 << (i & 7)

    def _getbit(self, i: int) -> bool:
        return (self.bits[i >> 3] >> (i & 7)) & 1 == 1

    # ----- hashing (double hashing) -----
    def _indices(self, item) -> Iterable[int]:
        b = _to_bytes(item)
        h1 = int.from_bytes(hashlib.sha256(b).digest()[:8], "little")
        h2 = int.from_bytes(hashlib.blake2b(b, digest_size=16).digest()[:8], "little")
        # generate k indices: (h1 + i*h2) mod m
        # note: use modulo once per i; avoid negative by masking via % self.m
        for i in range(self.k):
            yield (h1 + i * h2) % self.m

    # ----- public API -----
    def add(self, item) -> None:
        for idx in self._indices(item):
            self._setbit(idx)
        self.count += 1

    def __contains__(self, item) -> bool:
        return all(self._getbit(idx) for idx in self._indices(item))

    # handy stats
    def fill_ratio(self) -> float:
        set_bits = sum(bin(byte).count("1") for byte in self.bits)
        return set_bits / self.m

    def fp_rate_estimate(self) -> float:
        # (1 - e^{-k*n/m})^k with n≈items inserted (count)
        return (1 - math.e ** (-self.k * self.count / self.m)) ** self.k
