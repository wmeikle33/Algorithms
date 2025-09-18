from typing import List

def build_sa(s: str) -> List[int]:
    """
    Suffix Array of s (0-indexed), returns permutation sa so that
    s[sa[0]:] < s[sa[1]:] < ... < s[sa[n-1]:]
    """
    n = len(s)
    k = 1
    # initial ranking by characters
    rank = list(map(ord, s))
    sa = list(range(n))
    tmp = [0] * n

    while True:
        # sort by (rank[i], rank[i+k]) using Python's Timsort (stable)
        sa.sort(key=lambda i: (rank[i], rank[i + k] if i + k < n else -1))

        # re-rank
        tmp[sa[0]] = 0
        for i in range(1, n):
            a, b = sa[i-1], sa[i]
            tmp[b] = tmp[a] + (
                (rank[a], rank[a + k] if a + k < n else -1) <
                (rank[b], rank[b + k] if b + k < n else -1)
            )
        rank, tmp = tmp, rank
        if rank[sa[-1]] == n - 1:
            break
        k <<= 1
    return sa

def build_lcp(s: str, sa: List[int]) -> List[int]:
    """
    Kasai's algorithm.
    LCP[i] = LCP(suffix at sa[i], suffix at sa[i-1]), LCP[0] = 0.
    """
    n = len(s)
    rank = [0] * n
    for i, p in enumerate(sa):
        rank[p] = i

    lcp = [0] * n
    h = 0
    for i in range(n):
        r = rank[i]
        if r == 0:
            h = 0
            continue
        j = sa[r - 1]
        while i + h < n and j + h < n and s[i + h] == s[j + h]:
            h += 1
        lcp[r] = h
        if h:
            h -= 1
    return lcp  # note: lcp[0] = 0, length n

# Optional: pattern search on SA (returns [start_idx, ...] where s[start:].startswith(pat))
def sa_search(s: str, sa: List[int], pat: str) -> List[int]:
    import bisect
    n = len(s)

    # Lower bound for pat
    def lb():
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if s[sa[mid]:].startswith(pat) or s[sa[mid]:] > pat:
                hi = mid
            else:
                lo = mid + 1
        return lo

    # Upper bound for pat by comparing prefix order
    def ub():
        lo, hi = 0, n
        # Compare only up to len(pat)
        def cmp_prefix(i):
            return s[sa[i]:sa[i] + len(pat)]
        while lo < hi:
            mid = (lo + hi) // 2
            if cmp_prefix(mid) <= pat:
                lo = mid + 1
            else:
                hi = mid
        return lo

    L, R = lb(), ub()
    return [sa[i] for i in range(L, R)]
