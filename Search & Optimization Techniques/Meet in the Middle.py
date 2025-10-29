from itertools import combinations

def all_subset_sums(arr):
    sums = []
    n = len(arr)
    for k in range(n + 1):
        for combo in combinations(arr, k):
            sums.append(sum(combo))
    return sums

def subset_sum_meet_in_the_middle(nums, target):
    n = len(nums)
    mid = n // 2

    left = nums[:mid]
    right = nums[mid:]

    left_sums = all_subset_sums(left)  

    right_sums = all_subset_sums(right)

    left_set = set(left_sums)
    
    for rs in right_sums:
        need = target - rs
        if need in left_set:
            return True  # found a subset whose total is target

    return False  # no subset hits exactly target
