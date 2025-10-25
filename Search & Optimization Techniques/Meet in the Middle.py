from itertools import combinations

def all_subset_sums(arr):
    """
    Return a list of sums of all subsets of arr.
    For arr of length m, this returns 2^m sums.
    """
    sums = []
    n = len(arr)
    # for each possible subset size k = 0..n
    for k in range(n + 1):
        for combo in combinations(arr, k):
            sums.append(sum(combo))
    return sums

def subset_sum_meet_in_the_middle(nums, target):
    n = len(nums)
    mid = n // 2

    left = nums[:mid]
    right = nums[mid:]

    # 1. all subset sums of left
    left_sums = all_subset_sums(left)  # list of ints

    # 2. all subset sums of right
    right_sums = all_subset_sums(right)

    # 3. Put left_sums into a set for O(1) lookup
    left_set = set(left_sums)

    # 4. For each sum on the right, see if we can pair it
    for rs in right_sums:
        need = target - rs
        if need in left_set:
            return True  # found a subset whose total is target

    return False  # no subset hits exactly target
