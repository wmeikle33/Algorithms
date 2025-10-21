def manacher_odd_even(s: str):
    n = len(s)
    # ----- odd palindromes -----
    odd = [0] * n
    l = r = -1  # current rightmost palindrome is (l..r)
    for i in range(n):
        k = 1 if i > r else min(odd[l + r - i], r - i + 1)
        while i - k >= 0 and i + k < n and s[i - k] == s[i + k]:
            k += 1
        odd[i] = k
        if i + k - 1 > r:
            l = i - k + 1
            r = i + k - 1

    # ----- even palindromes -----
    even = [0] * n
    l = r = -1
    for i in range(n):
        k = 0 if i > r else min(even[l + r - i + 1], r - i + 1)
        while i - k - 1 >= 0 and i + k < n and s[i - k - 1] == s[i + k]:
            k += 1
        even[i] = k
        if i + k - 1 > r:
            l = i - k
            r = i + k - 1
    return odd, even

def longest_palindrome(s: str) -> str:
    if not s:
        return ""
    odd, even = manacher_odd_even(s)
    # best odd
    best_len = 0
    best_l = best_r = 0
    for i, k in enumerate(odd):
        L, R = i - (k - 1), i + (k - 1)
        if R - L + 1 > best_len:
            best_len = R - L + 1
            best_l, best_r = L, R
    # best even
    for i, k in enumerate(even):
        L, R = i - k, i + k - 1
        if k > 0 and R - L + 1 > best_len:
            best_len = R - L + 1
            best_l, best_r = L, R
    return s[best_l:best_r + 1]

def count_palindromes(s: str) -> int:
    # total number of palindromic substrings
    odd, even = manacher_odd_even(s)
    # each radius contributes exactly its size
    return sum(odd) + sum(even)
