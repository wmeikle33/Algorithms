from typing import List

def build_lps(p: str) -> List[int]:
    lps = [0] * len(p)
    j = 0  
    for i in range(1, len(p)):
        while j > 0 and p[i] != p[j]:
            j = lps[j - 1]
        if p[i] == p[j]:
            j += 1
            lps[i] = j
    return lps

def kmp_search(text: str, pattern: str) -> List[int]:
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1))

    lps = build_lps(pattern)
    res = []
    j = 0 
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = lps[j - 1]
        if text[i] == pattern[j]:
            j += 1
            if j == m:
                res.append(i - m + 1)
                j = lps[j - 1]  
    return res

def kmp_find_first(text: str, pattern: str) -> int:
    hits = kmp_search(text, pattern)
    return hits[0] if hits else -1

def kmp_count(text: str, pattern: str) -> int:
    return len(kmp_search(text, pattern))
