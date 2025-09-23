import random
from typing import Optional

class Node:
    __slots__ = ("key", "prio", "cnt", "size", "left", "right")
    def __init__(self, key: int):
        self.key = key
        self.prio = random.getrandbits(31) 
        self.cnt  = 1                     
        self.size = 1                      
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None

def _sz(t: Optional[Node]) -> int:
    return t.size if t else 0

def _upd(t: Optional[Node]) -> None:
    if t:
        t.size = t.cnt + _sz(t.left) + _sz(t.right)

def _rot_right(p: Node) -> Node:
    q = p.left
    p.left = q.right
    q.right = p
    _upd(p); _upd(q)
    return q

def _rot_left(p: Node) -> Node:
    q = p.right
    p.right = q.left
    q.left = p
    _upd(p); _upd(q)
    return q

def insert(t: Optional[Node], key: int) -> Node:
    if not t:
        return Node(key)
    if key == t.key:
        t.cnt += 1
    elif key < t.key:
        t.left = insert(t.left, key)
        if t.left and t.left.prio < t.prio:
            t = _rot_right(t)
    else:
        t.right = insert(t.right, key)
        if t.right and t.right.prio < t.prio:
            t = _rot_left(t)
    _upd(t)
    return t

def erase(t: Optional[Node], key: int) -> Optional[Node]:
    if not t: 
        return None
    if key == t.key:
        if t.cnt > 1:
            t.cnt -= 1
        else:
            # rotate a child up (the smaller priority wins)
            if not t.left:
                return t.right
            if not t.right:
                return t.left
            if t.left.prio < t.right.prio:
                t = _rot_right(t)
                t.right = erase(t.right, key)
            else:
                t = _rot_left(t)
                t.left = erase(t.left, key)
    elif key < t.key:
        t.left = erase(t.left, key)
    else:
        t.right = erase(t.right, key)
    _upd(t)
    return t

def find(t: Optional[Node], key: int) -> bool:
    while t:
        if key == t.key: return True
        t = t.left if key < t.key else t.right
    return False

def kth(t: Optional[Node], k: int) -> int:
    """1-based k-th smallest; raises IndexError if k out of range."""
    if not t or k <= 0 or k > _sz(t): 
        raise IndexError("k out of range")
    left = _sz(t.left)
    if k <= left:
        return kth(t.left, k)
    if k <= left + t.cnt:
        return t.key
    return kth(t.right, k - left - t.cnt)

def rank(t: Optional[Node], x: int) -> int:
    """# of elements strictly less than x."""
    res = 0
    while t:
        if x <= t.key:
            t = t.left
        else:
            res += _sz(t.left) + t.cnt
            t = t.right
    return res

def lower_bound(t: Optional[Node], x: int) -> Optional[int]:
    """Smallest key >= x; None if no such key."""
    ans = None
    while t:
        if x <= t.key:
            ans = t.key
            t = t.left
        else:
            t = t.right
    return ans
