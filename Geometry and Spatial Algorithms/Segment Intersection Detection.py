from typing import Optional, Tuple, Union
import math

Point = Tuple[float, float]
Overlap = Tuple[Point, Point]  # overlapping segment (collinear case)

EPS = 1e-9

def _sub(a: Point, b: Point) -> Point:
    return (a[0] - b[0], a[1] - b[1])

def _cross(a: Point, b: Point) -> float:
    return a[0]*b[1] - a[1]*b[0]

def _dot(a: Point, b: Point) -> float:
    return a[0]*b[0] + a[1]*b[1]

def _on_segment(a: Point, b: Point, p: Point) -> bool:
    # assuming a, b, p are collinear; check if p is within the bounding box of a-b
    return (min(a[0], b[0]) - EPS <= p[0] <= max(a[0], b[0]) + EPS and
            min(a[1], b[1]) - EPS <= p[1] <= max(a[1], b[1]) + EPS)

def segments_intersect(
    p: Point, p2: Point, q: Point, q2: Point
) -> Union[None, Point, Tuple[str, Overlap]]:
    """
    Returns:
      - None: no intersection
      - (x, y): single intersection point (including endpoint touch)
      - ('overlap', ((x1,y1),(x2,y2))): collinear overlapping segment (endpoints sorted)
    """
    r = _sub(p2, p)
    s = _sub(q2, q)
    rxs = _cross(r, s)
    q_p = _sub(q, p)
    qpxr = _cross(q_p, r)

    if abs(rxs) < EPS and abs(qpxr) < EPS:
        # Collinear: project onto an axis to find overlap
        # Use dot products along r to get scalar parameters for q and q2
        rr = _dot(r, r)
        if rr < EPS:
            # p == p2 (degenerate)
            return p if math.hypot(q[0]-p[0], q[1]-p[1]) < EPS else None
        t0 = _dot(q_p, r) / rr
        t1 = t0 + _dot(s, r) / rr
        tmin, tmax = sorted((t0, t1))
        # overlap exists if [tmin, tmax] intersects [0,1]
        if tmax < -EPS or tmin > 1+EPS:
            return None
        # clamp to [0,1] and map back to points
        a = (p[0] + max(0.0, tmin)*r[0], p[1] + max(0.0, tmin)*r[1])
        b = (p[0] + min(1.0, tmax)*r[0], p[1] + min(1.0, tmax)*r[1])
        # if it collapses to a point, return that point
        if math.hypot(a[0]-b[0], a[1]-b[1]) < EPS:
            return a
        # sort endpoints for consistency
        return ('overlap', tuple(sorted((a, b))))
    if abs(rxs) < EPS and abs(qpxr) >= EPS:
        # Parallel, non-intersecting
        return None

    # Lines intersect at p + t*r = q + u*s
    t = _cross(q_p, s) / rxs
    u = _cross(q_p, r) / rxs

    if -EPS <= t <= 1+EPS and -EPS <= u <= 1+EPS:
        # Intersection point
        pt = (p[0] + t*r[0], p[1] + t*r[1])
        return pt

    return None
