from typing import List, Tuple

def max_non_overlapping(intervals: List[Tuple[int,int]]) -> int:
    intervals.sort(key=lambda x: x[1])   # end time
    cnt, last_end = 0, float('-inf')
    for s, e in intervals:
        if s >= last_end:
            cnt += 1
            last_end = e
    return cnt
