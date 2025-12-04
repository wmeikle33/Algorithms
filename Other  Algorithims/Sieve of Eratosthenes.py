max_val = max(nums)
is_prime = [True] * (max_val + 1)
is_prime[0] = is_prime[1] = False
for i in range(2, int(max_val **.5)+1):
    if is_prime[i]:
        step = i
        start = i * i
        for j in range(start, max_val + 1, step):
            is_prime[j] = False
