import math, hashlib
from typing import Iterable

def _to_bytes(x) -> bytes:
    if isinstance(x, bytes):
        return x
    if isinstance(x, str):
        return x.encode("utf-8")
    return str(x).encode("utf-8")

def _calc_m_k(n: int, p: float) -> tuple[int, int]:
    m = math.ceil(-n * math.log(p) / (math.log(2) ** 2))
    k = max(1, round((m / n) * math.log(2)))
    return m, k

class BloomFilter:
    def __init__(self, m: int, k: int):
        self.m = m                    
        self.k = k                     
        self.bits = bytearray((m + 7) // 8)
        self.count = 0              

    @classmethod
    def from_params(cls, n: int, p: float = 0.01) -> "BloomFilter":
        m, k = _calc_m_k(n, p)
        return cls(m, k)

    def _setbit(self, i: int) -> None:
        self.bits[i >> 3] |= 1 << (i & 7)

    def _getbit(self, i: int) -> bool:
        return (self.bits[i >> 3] >> (i & 7)) & 1 == 1

    def _indices(self, item) -> Iterable[int]:
        b = _to_bytes(item)
        h1 = int.from_bytes(hashlib.sha256(b).digest()[:8], "little")
        h2 = int.from_bytes(hashlib.blake2b(b, digest_size=16).digest()[:8], "little")
        for i in range(self.k):
            yield (h1 + i * h2) % self.m

    def add(self, item) -> None:
        for idx in self._indices(item):
            self._setbit(idx)
        self.count += 1

    def __contains__(self, item) -> bool:
        return all(self._getbit(idx) for idx in self._indices(item))

    def fill_ratio(self) -> float:
        set_bits = sum(bin(byte).count("1") for byte in self.bits)
        return set_bits / self.m

    def fp_rate_estimate(self) -> float:
        return (1 - math.e ** (-self.k * self.count / self.m)) ** self.k
