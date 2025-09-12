from typing import List

class CombMod:
    """Precompute factorials, inverse factorials, and (optionally) all inverses mod a prime."""
    def __init__(self, N: int, MOD: int = 1_000_000_007, precompute_inv: bool = True):
        assert MOD > 1
        self.MOD = MOD
        self.N = N
        self.fact = [1]*(N+1)
        for i in range(1, N+1):
            self.fact[i] = self.fact[i-1]*i % MOD

        # invfact via one pow + downward sweep
        self.invfact = [1]*(N+1)
        self.invfact[N] = pow(self.fact[N], MOD-2, MOD)   # Fermat
        for i in range(N, 0, -1):
            self.invfact[i-1] = self.invfact[i]*i % MOD

        # Optional: all modular inverses 1..N in O(N) (handy for fractions)
        self.inv = None
        if precompute_inv:
            inv = [0]*(N+1)
            inv[1] = 1
            for i in range(2, N+1):
                inv[i] = MOD - (MOD//i) * inv[MOD % i] % MOD
            self.inv = inv

    def nCk(self, n: int, k: int) -> int:
        if k < 0 or k > n or n > self.N: return 0
        return self.fact[n] * self.invfact[k] % self.MOD * self.invfact[n-k] % self.MOD

    def nPk(self, n: int, k: int) -> int:
        if k < 0 or k > n or n > self.N: return 0
        return self.fact[n] * self.invfact[n-k] % self.MOD

    def multichoose(self, n: int, k: int) -> int:
        """Combinations with repetition: C(n+k-1, k)."""
        return self.nCk(n+k-1, k)
