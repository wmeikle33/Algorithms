def binary_search_min_true(lo: int, hi: int, ok) -> int:
    """Search on integers in [lo, hi] for the smallest x with ok(x)=True."""
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
