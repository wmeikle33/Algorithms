from typing import List

def build_lps(p: str) -> List[int]:
    """
    LPS[i] = length of the longest proper prefix of p[:i+1] which is also a suffix.
    """
    lps = [0] * len(p)
    j = 0  # length of current border
    for i in range(1, len(p)):
        while j > 0 and p[i] != p[j]:
            j = lps[j - 1]
        if p[i] == p[j]:
            j += 1
            lps[i] = j
    return lps

def kmp_search(text: str, pattern: str) -> List[int]:
    """
    Return all start indices where 'pattern' occurs in 'text' (overlapping allowed).
    If pattern is empty, return all positions (0..len(text)).
    """
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1))

    lps = build_lps(pattern)
    res = []
    j = 0  # index in pattern
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = lps[j - 1]
        if text[i] == pattern[j]:
            j += 1
            if j == m:
                res.append(i - m + 1)
                j = lps[j - 1]  # continue searching (supports overlaps)
    return res

# Convenience helpers
def kmp_find_first(text: str, pattern: str) -> int:
    """Return the first index of pattern in text, or -1 if not found."""
    hits = kmp_search(text, pattern)
    return hits[0] if hits else -1

def kmp_count(text: str, pattern: str) -> int:
    """Return the number of (possibly overlapping) occurrences."""
    return len(kmp_search(text, pattern))
