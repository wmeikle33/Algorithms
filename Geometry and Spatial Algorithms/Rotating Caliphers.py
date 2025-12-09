from __future__ import annotations
from typing import List, Tuple
import math
Point = Tuple[float, float]

def cross(ax: float, ay: float, bx: float, by: float) -> float:
    return ax * by - ay * bx

def cross_pts(o: Point, a: Point, b: Point) -> float:
    return cross(a[0] - o[0], a[1] - o[1], b[0] - o[0], b[1] - o[1])

def dist2(a: Point, b: Point) -> float:
    dx, dy = a[0] - b[0], a[1] - b[1]
    return dx*dx + dy*dy

def convex_hull(points: List[Point]) -> List[Point]:
    pts = sorted(set(points))
    if len(pts) <= 1:
        return pts[:]

    lower = []
    for p in pts:
        while len(lower) >= 2 and cross_pts(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross_pts(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Concatenate (omit last because it’s the start of the other list)
    hull = lower[:-1] + upper[:-1]
    return hull

def rotating_calipers_diameter(hull: List[Point]) -> Tuple[float, Tuple[Point, Point]]:
    m = len(hull)
    if m == 0:
        return 0.0, ((0.0, 0.0), (0.0, 0.0))
    if m == 1:
        return 0.0, (hull[0], hull[0])
    if m == 2:
        d = math.dist(hull[0], hull[1])
        return d, (hull[0], hull[1])

    j = 1
    best_d2 = 0.0
    best_pair = (hull[0], hull[0])

    def area2(i: int, j: int, k: int) -> float:
        return abs(cross_pts(hull[i], hull[j], hull[k]))

    for i in range(m):
        ni = (i + 1) % m
        while area2(i, ni, (j + 1) % m) > area2(i, ni, j):
            j = (j + 1) % m

        for a, b in ((i, j), (ni, j)):
            d2 = dist2(hull[a], hull[b])
            if d2 > best_d2:
                best_d2 = d2
                best_pair = (hull[a], hull[b])

    return math.sqrt(best_d2), best_pair
