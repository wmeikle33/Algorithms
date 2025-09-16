from typing import List, Tuple

Point = Tuple[float, float]

def convex_hull(points: List[Point], include_collinear: bool = False) -> List[Point]:
    pts = sorted(set(points))          # sort by x, then y; remove duplicates
    if len(pts) <= 1:
        return pts.copy()

    def cross(o: Point, a: Point, b: Point) -> float:
        # cross product (OA x OB): >0 = left turn, <0 = right turn, 0 = collinear
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    def build_half(seq):
        half = []
        for p in seq:
            # Pop while we turn "right" (or non-left). To keep collinear, only pop on right turns.
            while len(half) >= 2 and (
                cross(half[-2], half[-1], p) <= 0 if not include_collinear
                else cross(half[-2], half[-1], p) < 0
            ):
                half.pop()
            half.append(p)
        return half

    lower = build_half(pts)
    upper = build_half(reversed(pts))

    hull = lower[:-1] + upper[:-1]     # remove duplicated endpoints

    if include_collinear:
        # Remove accidental consecutive duplicates if any (rare)
        cleaned = []
        for p in hull:
            if not cleaned or cleaned[-1] != p:
                cleaned.append(p)
        hull = cleaned

    return hull
