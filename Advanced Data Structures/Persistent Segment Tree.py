from bisect import bisect_left, bisect_right
from typing import Optional, List

class Node:
    __slots__ = ("left", "right", "val")
    def __init__(self, left: Optional["Node"]=None, right: Optional["Node"]=None, val: int=0):
        self.left = left
        self.right = right
        self.val = val

def _upd(root: Optional[Node], l: int, r: int, idx: int, delta: int) -> Node:
    if l == r:
        return Node(None, None, (root.val if root else 0) + delta)
    mid = (l + r) // 2
    left = root.left if root else None
    right = root.right if root else None
    if idx <= mid:
        nl = _upd(left, l, mid, idx, delta)
        nr = right
    else:
        nl = left
        nr = _upd(right, mid + 1, r, idx, delta)
    return Node(nl, nr, (nl.val if nl else 0) + (nr.val if nr else 0))

def _sum(root: Optional[Node], l: int, r: int, ql: int, qr: int) -> int:
    if not root or qr < l or r < ql:
        return 0
    if ql <= l and r <= qr:
        return root.val
    mid = (l + r) // 2
    return _sum(root.left, l, mid, ql, qr) + _sum(root.right, mid + 1, r, ql, qr)

def _kth(root_r: Optional[Node], root_lm1: Optional[Node], l: int, r: int, k: int) -> int:
    if l == r:
        return l
    mid = (l + r) // 2
    left_r = root_r.left.val if (root_r and root_r.left) else 0
    left_l = root_lm1.left.val if (root_lm1 and root_lm1.left) else 0
    cnt_left = left_r - left_l
    if k <= cnt_left:
        return _kth(root_r.left if root_r else None,
                    root_lm1.left if root_lm1 else None, l, mid, k)
    return _kth(root_r.right if root_r else None,
                root_lm1.right if root_lm1 else None, mid + 1, r, k - cnt_left)

class PersistentSegTree:
    def __init__(self, arr: List[int]):
        self.arr = arr
        self.coord = sorted(set(arr))
        self.M = len(self.coord)
        self.versions: List[Optional[Node]] = [None]
        root = None
        for x in arr:
            idx = bisect_left(self.coord, x)
            root = _upd(root, 0, self.M - 1, idx, +1)
            self.versions.append(root)

    def sum_version(self, ver: int, Lval, Rval) -> int:
        if self.M == 0: return 0
        li = bisect_left(self.coord, Lval)
        ri = bisect_right(self.coord, Rval) - 1
        if li > ri: return 0
        return _sum(self.versions[ver], 0, self.M - 1, li, ri)

    def count_in_subarray_leq(self, L: int, R: int, x) -> int:
        if self.M == 0: return 0
        ri = bisect_right(self.coord, x) - 1
        if ri < 0: return 0
        if ri >= self.M: ri = self.M - 1
        verR = self.versions[R + 1]
        verL = self.versions[L]
        return _sum(verR, 0, self.M - 1, 0, ri) - _sum(verL, 0, self.M - 1, 0, ri)

    def kth_in_subarray(self, L: int, R: int, k: int):
        total = R - L + 1
        if not (1 <= k <= total):
            raise ValueError("k out of range")
        idx = _kth(self.versions[R + 1], self.versions[L], 0, self.M - 1, k)
        return self.coord[idx]
