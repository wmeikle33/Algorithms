def z_function(s: str) -> list[int]:
    n = len(s)
    z = [0] * n
    L = R = 0
    for i in range(1, n):
        if i <= R:
            z[i] = min(R - i + 1, z[i - L])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > R:
            L, R = i, i + z[i] - 1
    return z
