from itertools import accumulate

def build_prefix_sums(a):
    # ps[i] = sum of a[0..i-1]; ps has length len(a)+1
    return [0] + list(accumulate(a))

def range_sum(ps, l, r):
    """Sum of a[l..r] inclusive."""
    return ps[r + 1] - ps[l]

# Example
a = [2, -1, 3, 5, 4]
ps = build_prefix_sums(a)
assert range_sum(ps, 1, 3) == (-1 + 3 + 5)  # 7


# -----------------------------
# 2) Prefix Sums (2D)
# -----------------------------
def build_prefix_sums_2d(mat):
    m, n = len(mat), len(mat[0])
    ps = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            ps[i + 1][j + 1] = (
                ps[i][j + 1] + ps[i + 1][j] - ps[i][j] + mat[i][j]
            )
    return ps

def rect_sum(ps, r1, c1, r2, c2):
    """Sum over rectangle with corners (r1,c1)..(r2,c2), inclusive."""
    return (
        ps[r2 + 1][c2 + 1]
        - ps[r1][c2 + 1]
        - ps[r2 + 1][c1]
        + ps[r1][c1]
    )

# Example
mat = [
    [1, 2, 3],
    [4, 5, 6],
]
ps2 = build_prefix_sums_2d(mat)
assert rect_sum(ps2, 0, 1, 1, 2) == (2 + 3 + 5 + 6)  # 16

