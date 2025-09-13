from typing import List, Tuple

def union_area(rects: List[Tuple[int,int,int,int]]) -> int:
    """
    rects: list of (x1, y1, x2, y2) with x1 < x2, y1 < y2 (integers or floats)
    Returns total area covered by the union of rectangles.
    Sweep along x; maintain covered y-length with a segment tree over compressed y.
    """
    # 1) Build events (x, type, y1, y2), type=+1 add, -1 remove
    events = []
    ys = set()
    for x1, y1, x2, y2 in rects:
        events.append((x1, +1, y1, y2))
        events.append((x2, -1, y1, y2))
        ys.add(y1); ys.add(y2)
    events.sort()  # by x
    yvals = sorted(ys)

    # 2) Coordinate compression for y; segments are between consecutive yvals
    idx = {y:i for i, y in enumerate(yvals)}
    # Segment tree over [0..m-2], each leaf spans [yvals[i], yvals[i+1])
    m = len(yvals)
    if m < 2:
        return 0

    # Tree arrays
    cover = [0] * (4 * (m - 1))       # how many rectangles cover this segment
    length = [0.0] * (4 * (m - 1))    # covered length in y for this segment

    def pull(node: int, l: int, r: int):
        if cover[node] > 0:
            length[node] = yvals[r+1] - yvals[l]   # fully covered
        elif l == r:
            length[node] = 0.0
        else:
            length[node] = length[node*2] + length[node*2+1]

    def update(node: int, l: int, r: int, ql: int, qr: int, delta: int):
        if qr < l or r < ql:
            return
        if ql <= l and r <= qr:
            cover[node] += delta
            pull(node, l, r)
            return
        mid = (l + r) // 2
        update(node*2, l, mid, ql, qr, delta)
        update(node*2+1, mid+1, r, ql, qr, delta)
        pull(node, l, r)

    area = 0.0
    prev_x = events[0][0]
    for x, typ, y1, y2 in events:
        dx = x - prev_x
        if dx:
            area += length[1] * dx
            prev_x = x
        # apply all intervals starting/ending at this x
        i1, i2 = idx[y1], idx[y2] - 1  # inclusive range of segments
        if i1 <= i2:
            update(1, 0, m-2, i1, i2, typ)

    return area
