from typing import List

def rabin_karp(text: str, pat: str) -> int:
    n, m = len(text), len(pat)
    if m == 0: return 0
    if m > n:  return -1

    M = 1_000_000_007
    B = 911382323  
    Bm = pow(B, m, M)

    hp = 0
    hw = 0
    for i in range(m):
        hp = (hp * B + ord(pat[i])) % M
        hw = (hw * B + ord(text[i])) % M

    if hw == hp and text[:m] == pat:
        return 0

    for i in range(m, n):
        hw = (hw * B + ord(text[i]) - ord(text[i - m]) * Bm) % M
        if hw < 0: hw += M
        if hw == hp and text[i - m + 1:i + 1] == pat:
            return i - m + 1
    return -1
